from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Product
from .serializers import ProductSerializer

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