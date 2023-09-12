# Will be used for User Role Based Permissions & Authentication
from django.http import HttpResponse
from django.shortcuts import HttpResponse, redirect

# To stop an authenticated user from viewing the login and registration page
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs ):
         if request.user.is_authenticated:
            return redirect('home')
         else:
             return view_func(request, *args, **kwargs)
    
    return wrapper_func

# for the other views/pages that requires different roles
# It passes the users, then the function, then other conditions if you want
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator


# admin only decorator for the home view to restrict the user from seeing it
# checks user group, & sends user to customer page while it leaves admin on the page
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
        # Handle other cases, e.g., if group is not recognized
        return HttpResponse("You are not authorized to view this page", status=403)  # Return a forbidden response
    
    return wrapper_function
