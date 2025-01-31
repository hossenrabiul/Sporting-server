from rest_framework import serializers
from .models import Products

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ["author",]