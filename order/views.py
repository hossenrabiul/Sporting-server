from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from posts.models import Products
from . models import Order, Cart
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializers, OrderSerializers
# Create your views here.

class AddToCardView(APIView):
    def post(self, request, product_id):

        item = get_object_or_404(Products, pk=product_id)
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderItem.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                # messages.info(request, "This item quantity was updated!")
                return Response({"message": "This item quantity was updated!"}, status=status.HTTP_200_OK)
                return redirect('shop:home')
            else:
                order.orderItem.add(order_item[0])
                # messages.info(request, "This item was added to your cart!")
                return Response({"message": "This item was added to your cart!"}, status=status.HTTP_200_OK)
                return redirect('shop:home')
        else:
            order = Order(user=request.user)
            order.save()
            order.orderItem.add(order_item[0])
            # messages.info(request, "This item was added to your cart!")
            return Response({"message": "This item was added to your cart!"}, status=status.HTTP_200_OK)
            return redirect('shop:home')

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
    


    


