from django.db import models
from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField

class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey('userauth.UserProfile', on_delete=models.CASCADE)
    address1 = AddressField()
    address2 = AddressField(related_name='+', blank=True, null=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return str(self.id) + ": " + self.name

class Category(models.Model):
    name = models.CharField(max_length=30)
    restaurant = models.ForeignKey('Restaurant', related_name="restaurant", on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return str(self.id) + ": " + self.restaurant.name + " / " + self.name

class MenuItem(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    item_name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places = 2, max_digits=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ": " + self.category.restaurant.name + " / " + self.category.name +  " / " + self.item_name
