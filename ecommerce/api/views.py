from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Product
from .serializers import ProductSerializer

@api_view(["GET"])
def products(request):
    products = Product.objects.filter().prefetch_related('images')
    serializer = ProductSerializer(products,many=True,context={"request":request})
    return Response(serializer.data)