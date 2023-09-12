from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory #creates multiple forms within one form
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Order, Customer, Product
from .templates.accounts.forms import OrderForm, CreateUserForm
from .filters import OrderFilter


# Register
#The first if statement restricts the user to home page if they're not logged out
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        
        #when you save it creates user. The below hashes passwords for us
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)
                return redirect('login')

        context = {'form':form}
        return render(request, "accounts/register.html", context)

# login
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, "accounts/login.html", context)

# logout
def logoutUser(request):
    logout(request)
    return redirect('login')

# home page
@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {"orders":orders, "customers":customers, "total_orders":total_orders,
              "delivered":delivered, "pending":pending }

    return render(request, 'accounts/dashboard.html', context)

# products
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {"customer":customer, "orders":orders, "order_count":order_count, 'myFilter':myFilter}
    return render(request, 'accounts/customers.html', context)

#The below will use formsets to handle multiple instances of the Order model associated with customer
#Formsets simplify the process of managing and processing multiple forms on a single page, allowing the user to create multiple orders for a customer in a single submission
@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print("Printing POST:", request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        # save to db
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

# sends post data into the form and redirects you to dashboard
@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        # print("Printing POST:", request.POST)
        form = OrderForm(request.POST, instance=order)
        # save to db
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, "accounts/delete.html", context)