from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    info = models.TextField()

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")