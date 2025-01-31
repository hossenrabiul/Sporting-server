from django.db import models
from django.contrib.auth.models import User
from posts.models import Products
# Create your models here.
class Cart(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchaed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        total = self.product.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total
    
    
class Order(models.Model):
    orderItem = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    payment_id  = models.CharField(max_length=250, blank=True, null=True)
    ordered_id  = models.CharField(max_length=250, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_items in self.orderItem.all():
            total += order_items
        return total