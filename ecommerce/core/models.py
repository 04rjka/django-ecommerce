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
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("product","user")

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def cart_total(self):
        return sum(item.total_price() for item in self.items.all())
    def __str__(self):
        return f"{self.user.username}'s Cart"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    class Meta:
        unique_together = ("cart","product")
    
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="addresses")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150,blank=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.last_name}, {self.address_line_1}, {str(self.pincode)}"
