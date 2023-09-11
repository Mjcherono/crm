from django.forms import ModelForm
from ...models import Order

# builds a form for model Order with all fields
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
