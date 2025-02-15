from django.db import models
from django.contrib.auth.models import User
from posts.models import Products
# Create your models here.
class Cart(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Products, on_delete=models.CASCADE)
    # quantity = models.IntegerField(default=1)
    # purchaed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)



STATUS_CHOICES = [
         ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('rejected', 'Rejected'),
    ]
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    ordered_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending' ,blank=True,null=True)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',null=True,blank=True)

    def __str__(self):
        return f"{self.product.name} - ({self.quantity}) -  {self.status}"