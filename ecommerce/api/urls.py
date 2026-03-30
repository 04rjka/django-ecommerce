from django.urls import path
from . import views

urlpatterns = [
    path("products/",views.products,name="api_products"),
    path("product/<int:pk>/",views.product,name="api_product"),
]