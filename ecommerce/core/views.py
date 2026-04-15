from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserForm,UserLoginForm,ProductForm,ProductImageFormSet,ProductReviewForm,AddressForm,ProductVariantFormSet
from django.contrib import messages
from .models import Product,Cart,CartItem,Address,Order,OrderItem,ProductVariant
from django.db.models import Q
from django.conf import settings
import requests
import uuid

CASHFREE_BASE_URL = (
    'https://sandbox.cashfree.com/pg'
    if settings.CASHFREE_ENV == 'TEST'
    else 'https://api.cashfree.com/pg'
)

def get_headers():
    return {
        'x-client-id': settings.CASHFREE_APP_ID,
        'x-client-secret': settings.CASHFREE_SECRET_KEY,
        'x-api-version': '2025-01-01',   # latest version from docs
        'Content-Type': 'application/json',
    }

def home(request):
    products = Product.objects.prefetch_related("images")
    query = request.GET.get("q","")
    if query:
        products = products.filter(
            Q(name__icontains=query)|
            Q(info__icontains=query)
        ).distinct()
    featured = products.filter(is_featured=True)
    return render(request,"core/home.html",{"products":products,"query":query,"featured":featured})

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
            else:
                messages.error(request,"Incorrect Username or Password.")
    form = UserLoginForm()
    return render(request,"core/login.html",{"form":form})

def customer_logout(request):
    logout(request)
    return redirect("customer_login")

@staff_member_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductVariantFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect("add_images",pk=product.pk)
    else:
        form = ProductForm()
        formset = ProductVariantFormSet()
    return render(request,"core/add_product.html",{"form":form,"formset":formset})

@staff_member_required
def add_product_images(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == "POST":
        formset = ProductImageFormSet(request.POST,request.FILES,instance=product,form_kwargs={"product":product})
        if formset.is_valid():
            formset.save()
            return redirect("staff_home")
    else:
        formset = ProductImageFormSet(instance=product,form_kwargs={"product":product})
    return render(request,"core/add_product_images.html",{
        "product":product,
        "formset":formset
    })


def product_page(request,pk):
    product = Product.objects.prefetch_related("images","reviews").get(pk=pk)
    variants = ProductVariant.objects.filter(product=product)
    # print(variants)
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
    return render(request,"core/product_page.html",{"product":product,"form":form,"already_reviewed":already_reviewed,"variants":variants})

@login_required
def profile(request):
    user = request.user
    return render(request,"core/profile.html",{"user":user})

@login_required
def add_to_cart(request,pk):
    product = Product.objects.get(pk=pk)
    variant_id = request.POST.get("variant_id")
    quantity = int(request.POST.get("quantity",1))
    variant = ProductVariant.objects.get(id = variant_id, product=product)
    cart , created = Cart.objects.get_or_create(user = request.user)
    cart_item,item_created = CartItem.objects.get_or_create(cart = cart,product=product,variant=variant)
    if not item_created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

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
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        address = addresses.get(pk=address_id)
        order = Order.objects.create(
            user=request.user,
            name = f"{address.first_name} {address.last_name}",
            address_line_1 = address.address_line_1,
            address_line_2 = address.address_line_2,
            phone = address.phone,
            pincode = address.pincode,
            city = address.city,
            state = address.state,
            price = cart.cart_total()
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order = order,
                product = item.product,
                price = item.product.price,
                quantity = item.quantity,
                variant = item.variant
            )
        cart.delete()
        return redirect("initiate_payment",pk=order.pk)
            
    return render(request,"core/checkout.html",{"cart":cart,"addresses":addresses})

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

@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        next_url = request.GET.get("next")
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            if next_url:
                return redirect(next_url)
            return redirect("view_address")
    else:
        form = AddressForm()
    return render(request,"core/address.html",{"form":form})

@login_required
def view_address(request):
    addresses = Address.objects.filter(user = request.user) 
    return render(request,"core/user_address.html",{"addresses":addresses})

@login_required
def delete_address(request,pk):
    address = Address.objects.get(pk=pk)
    address.delete()
    return redirect("view_address")

@login_required
def order_success(request,pk):
    order = Order.objects.get(pk = pk,user=request.user)
    order_items = OrderItem.objects.filter(order=order).select_related("product")
    return render(request,"core/order_success.html",{"order":order,"order_items":order_items})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("orderitems__product").order_by("-pk")
    # order_items = OrderItem.objects.filter(order=order).select_related("product")
    return render(request,"core/orders.html",{"orders":orders})

@login_required
def order_details(request,pk):
    order = Order.objects.get(pk = pk,user=request.user)
    order_items = OrderItem.objects.filter(order=order).select_related("product")
    return render(request,"core/order_details.html",{"order":order,"order_items":order_items})

@login_required
def edit_address(request,pk):
    address = Address.objects.get(pk = pk)
    if request.method == "POST":
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("view_address")
    else:
        form = AddressForm(instance=address)
    return render(request,"core/edit_address.html",{"form":form})

@login_required
def initiate_payment(request,pk):
    order = Order.objects.get(pk=pk,user = request.user)

    payload = {
        'order_id': f'order_{order.id}',
        'order_amount': float(order.price),
        'order_currency': 'INR',
        'customer_details': {
            'customer_id': str(request.user.id),
            'customer_name': request.user.get_full_name() or request.user.username,
            'customer_email': request.user.email,
            'customer_phone': str(order.phone),  # using phone from order
        },
        'order_meta': {
            'return_url': request.build_absolute_uri('/payment/success/') + '?order_id={order_id}',
        }
    }

    response = requests.post(
        f'{CASHFREE_BASE_URL}/orders',
        json=payload,
        headers=get_headers()
    )

    data = response.json()

    if response.status_code == 200:
        order.cashfree_order_id = data["order_id"]
        order.save()

        return render(request, 'core/payment_checkout.html', {
            'session_id': data['payment_session_id'],
            'order': order,
            'env': 'sandbox' if settings.CASHFREE_ENV == 'TEST' else 'production',
        })
    else:
        messages.error(request, f"Payment initiation failed: {data.get('message', 'Unknown error')}")
        return redirect('order_details', pk=order.pk)

@login_required
def payment_success(request):
    cashfree_order_id = request.GET.get("order_id")

    if not cashfree_order_id:
        messages.error(request, "Invalid payment request.")
        print("Invalid payment request.")
        return redirect('orders')
    
    response = requests.get(
        f'{CASHFREE_BASE_URL}/orders/{cashfree_order_id}',
        headers=get_headers()
    )

    data = response.json()
    status = data.get('order_status')

    try:
        order = Order.objects.get(cashfree_order_id=cashfree_order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('orders')

    if status == 'PAID':
        order.payment_status = Order.PaymentStatus.PAID
        order.status = Order.Status.PLACED  # if you have status field
        order.save()
        return redirect('order_success', pk=order.pk)
    else:
        order.payment_status = Order.PaymentStatus.FAILED
        order.save()
        messages.error(request, "Payment failed or cancelled. Please try again.")
        return redirect('order_details', pk=order.pk)

@login_required
def cancel_order(request,pk):
    order = Order.objects.get(pk = pk, user=request.user)

    if order.status in ["shipped","delivered"]:
        messages.error(request,"Order cannot be cancelled after shipping.")
        return redirect("order_details",pk=pk)
    
    if order.status == "cancelled":
        messages.error(request,"Order already cancelled.")
        return redirect("order_details",pk=pk)
    
    if order.payment_status == Order.PaymentStatus.PAID:
        return redirect("refund_order",pk=pk)
    
    order.status = Order.Status.CANCELLED
    order.save()
    messages.success(request,"Order cancelled successfully.")
    return redirect("order_details",pk=pk)

@login_required
def refund_order(request,pk):
    order = Order.objects.get(pk=pk,user=request.user)

    if order.payment_status != Order.PaymentStatus.PAID:
        messages.error(request,"Only paid order can be refunded.")
        return redirect("order_details",pk=pk)
    
    if order.payment_status == Order.PaymentStatus.REFUNDED:
        messages.error(request,"Only has already been refunded.")
        return redirect("order_details",pk=pk)
    
    refund_id = f"refund_{order.id}_{uuid.uuid4().hex[:8]}"

    payload = {
        'refund_amount': float(order.price),      # full refund
        'refund_id': refund_id,                    # your unique refund id
        'refund_note': f'Cancellation refund for order #{order.id}',
        'refund_speed': 'STANDARD',                # or 'INSTANT'
    }

    response = requests.post(
        f'{CASHFREE_BASE_URL}/orders/{order.cashfree_order_id}/refunds',
        json=payload,
        headers=get_headers()
    )

    data = response.json()
    refund_status = data.get("refund_status")

    if response.status_code == 200:
        order.status = Order.Status.CANCELLED
        order.refund_id = refund_id

        if refund_status == "SUCCESS":
            order.payment_status = Order.PaymentStatus.REFUNDED
            messages.success(request,"Order cancelled and refund initiated successfully.")
        elif refund_status in ["ONHOLD","PENDING"]:
            order.payment_status = Order.PaymentStatus.REFUND_PENDING
            messages.error(request,"Refund is being processed. It may take 5-7 business days.")
        
        order.save()
        return redirect("order_details",pk=pk)
    else:
        messages.error(request, f"Refund failed: {data.get('message', 'Unknown error')}")
        return redirect('order_details', pk=pk)