from django.urls import path
from . import views

urlpatterns = [
    path("home/",views.home,name="home"),
    path("signup/",views.customer_signup,name="customer_signup"),
    path("",views.customer_login,name="customer_login"),
    path("logout/",views.customer_logout,name="customer_logout"),
    path("add/",views.add_product,name="add_product"),
    path("product/<int:pk>/",views.product_page,name="product_page"),
    path("profile/",views.profile,name="profile"),
]