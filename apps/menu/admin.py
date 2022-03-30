from tkinter import Menu
from django.contrib import admin
from .models import Restaurant, Category, MenuItem

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(MenuItem)