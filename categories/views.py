from django.shortcuts import render
from rest_framework import viewsets
from . models import Category, Brand
from . import serializers
# Create your views here.

class CategoriViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.categoriesSerializers

class BrandViewset(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = serializers.brandSerializers
