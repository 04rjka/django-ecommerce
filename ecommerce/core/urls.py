from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("signup/",views.customer_signup,name="customer_signup"),
]