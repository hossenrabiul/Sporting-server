from rest_framework import serializers
from . models import Category, Brand

class categoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class brandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'