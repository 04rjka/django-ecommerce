from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Product,ProductReview
from .serializers import ProductSerializer,ProductReviewSerializer

@api_view(["GET"])
def products(request):
    products = Product.objects.filter().prefetch_related('images')
    serializer = ProductSerializer(products,many=True,context={"request":request})
    return Response(serializer.data)

@api_view(["GET"])
def product(request,pk):
    query_set = Product.objects.prefetch_related("images")
    product = get_object_or_404(query_set,pk=pk)
    serializer = ProductSerializer(product,context={"request":request})
    return Response(serializer.data)

@api_view(["GET"])
def product_reviews(request,pk):
    product = get_object_or_404(Product,pk=pk)
    reviews =  ProductReview.objects.filter(product=product)
    serializer = ProductReviewSerializer(reviews,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
