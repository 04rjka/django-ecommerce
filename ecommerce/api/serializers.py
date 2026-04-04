from rest_framework import serializers
from core.models import Product,ProductImage,ProductReview

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id","image"]

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    class Meta:
        model = ProductReview
        fields = ["id","user","title","content","created_at"]