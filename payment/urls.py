from django.urls import path
from . import views
urlpatterns = [
  
    path('chekout/', views.CheckoutView.as_view(), name = 'checkout'),
    path('pay/', views.paymentView.as_view(), name = 'payment'),
    path('success/', views.successView, name = 'purchased'),
    path('cancel/', views.cancelView, name = 'purchased'),
   
]