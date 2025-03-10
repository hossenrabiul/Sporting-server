from django.db import models
from . constraint import STAR_CHOICES
from categories.models import Category
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    storkQuantity = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=201, blank=True, null=True)
    rating = models.TextField(choices=STAR_CHOICES)
    descirption = models.TextField()
    price = models.IntegerField()


class newProducts(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    storkQuantity = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=201, blank=True, null=True)
    rating = models.TextField(choices=STAR_CHOICES)
    descirption = models.TextField()
    price = models.IntegerField()
    