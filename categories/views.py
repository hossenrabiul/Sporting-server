from django.shortcuts import render
from rest_framework import viewsets
from . models import Category
from . import serializers
# Create your views here.

class CategoriViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.categoriesSerializers

