from django.forms import ModelForm
from .models import Restaurant, Category, MenuItem

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address1', 'address2', 'phone_number']