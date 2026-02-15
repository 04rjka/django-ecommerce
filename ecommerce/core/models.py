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
    product = models.ForeignKey(Product,related_name="images",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")

class ProductReview(models.Model):
    product = models.ForeignKey(Product,related_name="reviews",on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.CharField()
    created_at = models.DateTimeField(timezone.now)

    class Meta:
        unique_together = ("product","user")