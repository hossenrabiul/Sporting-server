from django.urls import path
from . import views
urlpatterns = [
    
    path('addToCard/<int:product_id>/', views.AddToCardView.as_view(), name = 'addtocard'),
    path('cart/', views.CartView.as_view(), name = 'cart'),
    path('cart/item/<int:item_id>/', views.CartView.as_view(), name = 'cart_item'),

    # path('pay/', views.PaymentView.as_view(), name = 'pay'),
    # path('pay/', views.PaymentView.as_view(), name = 'pay'),
   
]