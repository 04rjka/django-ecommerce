from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm,UserLoginForm
from django.contrib import messages

def home(request):
    return render(request,"core/home.html")

def customer_signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email already exists.")
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.save()
                messages.success(request,"Account created successfully.")
                return redirect("customer_signup")
    else:
        form = UserForm()
    return render(request,"core/signup.html",{"form":form})

def customer_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("home")
    form = UserLoginForm()
    return render(request,"core/login.html",{"form":form})

def customer_logout(request):
    logout(request)
    return redirect("customer_login")