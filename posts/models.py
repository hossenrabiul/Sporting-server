from django.db import models
from . constraint import STAR_CHOICES
from categories.models import Category, Brand
from django.contrib.auth.models import User
# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    storkQuantity = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images/uploads', blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    rating = models.TextField(choices=STAR_CHOICES)
    descirption = models.TextField()
    price = models.IntegerField()