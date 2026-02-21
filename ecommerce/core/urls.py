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
    path("addtocart/<int:pk>/",views.add_to_cart,name="add_to_cart"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("remove/<int:pk>",views.remove_cart_item,name="remove"),
    path("staffhome/",views.staff_home,name="staff_home"),
    path("staffproduct/<int:pk>/",views.staff_product_page,name="staff_product_page"),
    path("inc/<int:pk>",views.increment_cart_item,name="increment"),
    path("dec/<int:pk>",views.decrement_cart_item,name="decrement"),
]