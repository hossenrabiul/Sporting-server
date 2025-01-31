from django.urls import path
from . import views
urlpatterns = [
  
    path('chekout/', views.checkout, name = 'checkout'),
    path('pay/', views.paymentView, name = 'payment'),
    # path('purchased/', views.purchased, name = 'purchased'),
   
]