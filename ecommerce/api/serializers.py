from rest_framework import serializers
from core.models import Product,ProductImage,ProductReview,ProductVariant

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id","image"]

class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    class Meta:
        model = ProductReview
        fields = ["id","user","title","content","created_at"]

class ProductVariantSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True,read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ["id","name","stock","price","is_available" ,"images"]

    def get_price(self,obj):
        return obj.get_price()
        

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True,read_only=True)
    variants = ProductVariantSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = "__all__"