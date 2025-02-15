from django.urls import path
from . import views
urlpatterns = [
  
    path('pay/', views.PaymentAPI.as_view(), name = 'pay'),
    path('success/', views.PaymentSuccessAPI.as_view(), name = 'success'),
    path('fail/', views.PaymentFailedAPI.as_view(), name = 'failed'),
    path('cancel/', views.PaymentCancelAPI.as_view(), name = 'cancel'),
   
]