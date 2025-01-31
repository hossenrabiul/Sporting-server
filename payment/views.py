from django.shortcuts import render
from order.models import Cart, Order
from sslcommerz_lib import SSLCOMMERZ 
# Create your views here.

def checkout(request):
    order_qs = Order.objects.filter(user =request.user, ordered = False)
    order_items = order_qs.orderItem.all()

    order_total = order_qs.get_total()

    context = {
        'order_items' : order_items,
        'order_total' : order_total
    }
    return context


def paymentView(request):

    order_qs = Order.objects.filter(user =request.user, ordered = False)
    order_items = order_qs.orderItem.all()

    order_total = order_qs.get_total()

   
    settings = { 'store_id': 'devel679c32d3d4684', 'store_pass': 'devel679c32d3d4684@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = "http://127.0.0.1:8000/payment/purchased/"
    post_body['fail_url'] = "your fail url"
    post_body['cancel_url'] = "your cancel url"
    post_body['emi_option'] = 0
    post_body['cus_name'] = "test"
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    print(response)
    # Need to redirect user to response['GatewayPageURL']