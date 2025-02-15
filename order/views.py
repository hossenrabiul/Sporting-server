from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from posts.models import Products
from . models import Order, Cart, CartItems, OrderItem
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializers, OrderSerializers
from rest_framework.permissions import IsAdminUser
from django.db import transaction
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
        cart_items = Cart.objects.filter(user = request.user, ordered = False).first()
        if cart_items:
            serializer = CartSerializers(cart_items, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"Detail" : "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')


        product = get_object_or_404(Products, id = product_id)

        cart, created = Cart.objects.get_or_create(user = user, ordered = False)

        cart_item, item_created = CartItems.objects.get_or_create(
            cart = cart,
            product = product,
            defaults={"quantity" : quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
        serializer = CartSerializers(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, item_id):
        cart_item = get_object_or_404(CartItems, id = item_id, cart__user = request.user)
        quantity = request.data.get('quantity', cart_item.quantity)

        cart_item.quantity = quantity
        cart_item.save()

        cart = cart_item.cart
        serializer = CartSerializers(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, item_id):
        cart_item = get_object_or_404(CartItems, id = item_id, cart__user = request.user)
        cart_item.delete()

        cart = cart_item.cart
        serializer = CartSerializers(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CheckoutAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user, ordered=False)
        
        if cart.items.count() == 0:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total
        total = sum([item.product.price * item.quantity for item in cart.items.all()])

        order = Order.objects.create(
            user = user,
            total = total,
            status = 'pending'
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price,
            )
            
        cart.ordered = True
        cart.save()

        # Clear the cart
        cart.items.all().delete()

        return Response({"message": "Order placed successfully. Pending approval by admin."}, status=status.HTTP_201_CREATED)


# class PaymentView(APIView):
#     def post(self, request):
#         cart_items = Cart.objects.filter(user = request.user)
#         total = 0
#         for item in cart_items:
#             total += item.product.price * item.quantity
#         return Response('payment successfull', status=status.HTTP_200_OK)
    


    


