from django.shortcuts import render
from order.models import Cart, Order
from sslcommerz_lib import SSLCOMMERZ 

from django.http import HttpResponse ,JsonResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
from datetime import datetime

import uuid  # To generate unique transaction ID
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view 
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from order.serializers import OrderSerializers

class CheckoutView(APIView):
    def get(self, request):
        # Get the user's orders that are not yet ordered
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if not order_qs.exists():
            return Response(
                {'message': 'No active orders found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the order data
        serializer = OrderSerializers(order_qs, many=True)

        # Calculate the total order amount
        order_total = order_qs.first().get_total()

        # Return the response
        return Response({
            'orders': serializer.data,
            'order_total': order_total
        })


class paymenView(APIView):
    def post(self, request):
        # Extract data from the request (if needed)
        user_email = request.user.email if request.user.is_authenticated else "guest@example.com"

        # SSLCommerz settings
        settings = {
            'store_id': 'devel679c32d3d4684',
            'store_pass': 'devel679c32d3d4684@ssl',
            'issandbox': True
        }
        sslcz = SSLCOMMERZ(settings)

        # Prepare the payment request payload
        post_body = {
            'total_amount': 100.0,  # Replace with dynamic value if needed
            'currency': "BDT",
            'tran_id': "12345",  # Replace with a unique transaction ID
            'success_url': "http://127.0.0.1:8000/payment/success/",
            'fail_url': "http://127.0.0.1:8000/payment/cancelView/",
            'cancel_url': "http://127.0.0.1:8000/payment/cancelView/",
            'emi_option': 0,
            'cus_name': "test",
            'cus_email': user_email,
            'cus_phone': "01700000000",
            'cus_add1': "customer address",
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': "Test",
            'product_category': "Test Category",
            'product_profile': "general"
        }

        # Create a payment session
        try:
            response = sslcz.createSession(post_body)
            gateway_url = response.get('GatewayPageURL')

            if gateway_url:
                return Response({
                    'status': 'success',
                    'message': 'Payment session created successfully.',
                    'gateway_url': gateway_url
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Failed to create payment session.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            tran_id = str(uuid.uuid4())[:10] 

            settings = {
            'store_id': 'devel679c32d3d4684',
            'store_pass': 'devel679c32d3d4684@ssl',
            'issandbox': True
            }

            sslcz = SSLCOMMERZ(settings)

            post_body = {
                'total_amount': 5000,
                'currency': "BDT",
                'tran_id': tran_id,
                'success_url': "http://127.0.0.1:8000/payment/success/",
                'fail_url': "http://127.0.0.1:8000/payment/fail/",
                'cancel_url': "http://127.0.0.1:8000/payment/cancel/",
                'emi_option': 0,
                'cus_name':User.username,
                'cus_email':User.email,
                'cus_phone': "01765034196",
                'cus_add1': "Dhaka",
                'cus_city': "Dhaka",
                'cus_country': "Bangladesh", 
                'shipping_method': "NO",
                'multi_card_name': "10304040",
                'num_of_item': 1,
                'product_name': "Test",
                'product_category': "Test Category",
                'product_profile': "general",
            }

            response = sslcz.createSession(post_body)

            if 'GatewayPageURL' not in response:
                return Response({"error": "Payment session creation failed", "details": response}, status=400)

            return Response({'payment_url': response['GatewayPageURL']})

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class PaymentSuccessAPI(APIView):
    def post(self, request):
        return Response({"message": "Payment successful", "data": request.data})

class PaymentFailedAPI(APIView):
    def post(self, request):
        return Response({"message": "Payment failed", "data": request.data})


class PaymentCancelAPI(APIView):
    def post(self, request):
        return Response({"message": "Payment cancelled", "data": request.data})