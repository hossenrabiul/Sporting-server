from rest_framework import serializers
from .models import Products, newProducts

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ["author",]

class newPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = newProducts
        fields = '__all__'
        read_only_fields = ["author",]