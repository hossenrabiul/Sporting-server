from django.contrib import admin
from . models import Products, newProducts
# Register your models here.

admin.site.register(Products),
admin.site.register(newProducts)
