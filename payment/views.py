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


# def paymentView(request):

#     # order_qs = Order.objects.filter(user =request.user, ordered = False)
#     # order_items = order_qs.orderItem.all()

#     # order_total = order_qs.get_total()

   
#     settings = { 'store_id': 'devel679c32d3d4684', 'store_pass': 'devel679c32d3d4684@ssl', 'issandbox': True }
#     sslcz = SSLCOMMERZ(settings)
#     post_body = {}
#     post_body['total_amount'] = 100.0
#     post_body['currency'] = "BDT"
#     post_body['tran_id'] = "12345"
#     post_body['success_url'] = "http://127.0.0.1:8000/payment/successView/"
#     post_body['fail_url'] = "http://127.0.0.1:8000/payment/cancelView/"
#     post_body['cancel_url'] = "http://127.0.0.1:8000/payment/cancelView/"
#     post_body['emi_option'] = 0
#     post_body['cus_name'] = "test"
#     post_body['cus_email'] = "request.user.email"
#     post_body['cus_phone'] = "01700000000"
#     post_body['cus_add1'] = "customer address"
#     post_body['cus_city'] = "Dhaka"
#     post_body['cus_country'] = "Bangladesh"
#     post_body['shipping_method'] = "NO"
#     post_body['multi_card_name'] = ""
#     post_body['num_of_item'] = 1
#     post_body['product_name'] = "Test"
#     post_body['product_category'] = "Test Category"
#     post_body['product_profile'] = "general"


#     response = sslcz.createSession(post_body) # API response
#     print(response)
#     # Need to redirect user to response['GatewayPageURL']


class paymentView(APIView):
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


def successView(request):
    # Extract transaction details from the query parameters
    train_id = request.GET.get('train_id')
    status = request.GET.get('status')
    # user = User.objects.get(id = id)
    # order = Order.objects.get(user = user)
    # order.ordered = True
    # order.save()

    return HttpResponse(
        json.dumps({
            'status': 'success',
            'message': 'Payment completed successfully',
            'train_id' : train_id,
            'payment_status': status
        }),
        content_type='application/json'
    )

def cancelView(request):
    # Extract transaction details from the query parameters
    tran_id = request.GET.get('tran_id')
    status = request.GET.get('status')

    return HttpResponse(
        json.dumps({
            'status': 'cancelled',
            'message': 'Payment was cancelled',
            'tran_id': tran_id,
            'payment_status': status
        }),
        content_type='application/json'
    )
