from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserForm,UserLoginForm,ProductForm,ProductImageFormSet,ProductReviewForm
from django.contrib import messages
from .models import Product,Cart,CartItem

def home(request):
    products = Product.objects.prefetch_related("images")
    return render(request,"core/home.html",{"products":products})

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
                if user.is_staff:
                    print("STAFF")
                    return redirect("staff_home")
                return redirect("home")
    form = UserLoginForm()
    return render(request,"core/login.html",{"form":form})

def customer_logout(request):
    logout(request)
    return redirect("customer_login")

@staff_member_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductImageFormSet(request.POST,request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect("home")
    else:
        form = ProductForm()
        formset = ProductImageFormSet()
    return render(request,"core/add_product.html",{"form":form,"formset":formset})

def product_page(request,pk):
    product = Product.objects.prefetch_related("images","reviews").get(pk=pk)
    already_reviewed = product.reviews.filter(user=request.user).exists()
    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect("product_page",pk=pk)
    else:
        form = ProductReviewForm()
    return render(request,"core/product_page.html",{"product":product,"form":form,"already_reviewed":already_reviewed})

@login_required
def profile(request):
    user = request.user
    return render(request,"core/profile.html",{"user":user})

@login_required
def add_to_cart(request,pk):
    product = Product.objects.get(pk=pk)
    cart , created = Cart.objects.get_or_create(user = request.user)
    cart_item,item_created = CartItem.objects.get_or_create(cart = cart,product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("product_page",pk=pk)

@login_required
def cart(request):
    cart,_ = Cart.objects.get_or_create(user = request.user)
    cart = Cart.objects.prefetch_related("items__product__images").get(pk=cart.pk)
    return render(request,"core/cart.html",{"cart":cart})

@login_required
def checkout(request):
    cart,_ = Cart.objects.get_or_create(user = request.user)
    cart = Cart.objects.prefetch_related("items__product__images").get(pk=cart.pk)
            
    return render(request,"core/checkout.html",{"cart":cart})

@login_required
def remove_cart_item(request,pk):
    cart ,_ = Cart.objects.get_or_create(user = request.user)
    cart_items = Cart.objects.prefetch_related("items").get(pk = cart.pk)
    item = cart_items.items.get(pk=pk)
    print(item)
    item.delete()
    return redirect("cart")

@staff_member_required
def staff_home(request):
    products = Product.objects.prefetch_related("images")
    return render(request,"core/staff_home.html",{"products":products})

@staff_member_required
def staff_product_page(request,pk):
    product = Product.objects.prefetch_related("images","reviews").get(pk=pk)
    return render(request,"core/staff_product_page.html",{"product":product})

@login_required
def increment_cart_item(request,pk):
    cart ,_ = Cart.objects.get_or_create(user = request.user)
    cart_items = Cart.objects.prefetch_related("items").get(pk = cart.pk)
    item = cart_items.items.get(pk=pk)
    item.quantity += 1
    item.save()
    return redirect("cart")

@login_required
def decrement_cart_item(request,pk):
    cart ,_ = Cart.objects.get_or_create(user = request.user)
    cart_items = Cart.objects.prefetch_related("items").get(pk = cart.pk)
    item = cart_items.items.get(pk=pk)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")
