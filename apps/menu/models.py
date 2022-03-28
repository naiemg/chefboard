from django.db import models
from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    owner = models.ForeignKey('userauth.UserProfile', on_delete=models.CASCADE, blank=True, null=True)
    address1 = AddressField(blank=True, null=True)
    address2 = AddressField(related_name='+', blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
