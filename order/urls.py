from django.urls import path
from . import views
urlpatterns = [
    
    path('addToCard/<int:product_id>/', views.AddToCardView.as_view(), name = 'addtocard'),
    path('view/', views.CartView.as_view(), name = 'view'),
    path('pay/', views.PaymentView.as_view(), name = 'pay'),
    # path('pay/', views.PaymentView.as_view(), name = 'pay'),
   
]