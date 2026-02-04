from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm,UserLoginForm

def home(request):
    return render(request,"core/home.html")

def customer_signup(request):
    form = UserForm()
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            print(email,"Already Exists.")
            redirect("customer_signup")
        user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
        user.save()
    return render(request,"core/signup.html",{"form":form})

def customer_login(request):
    form = UserLoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
    
    return render(request,"core/login.html",{"form":form})