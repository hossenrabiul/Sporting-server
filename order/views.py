from django.shortcuts import render
from rest_framework.views import APIView
from posts.models import Products
from . models import Order, Cart
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializers, OrderSerializers
# Create your views here.

class AddToCardView(APIView):
    def post(self, request, product_id):
        product = Products.objects.get(id = product_id)
        cart_item, created = Cart.objects.get_or_create(user = request.user, product = product)
        if not created:
            cart_item.quantity += 1
            cart_item.product = product
            cart_item.user = request.user
            cart_item.save()
        return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)
    

class CartView(APIView):
    def get(self, request):
        cart_items = Cart.objects.filter(user = request.user)
        serializer = CartSerializers(cart_items, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class PaymentView(APIView):
    def post(self, request):
        cart_items = Cart.objects.filter(user = request.user)
        total = 0
        for item in cart_items:
            total += item.product.price * item.quantity
        return Response('payment successfull', status=status.HTTP_200_OK)
    


    


