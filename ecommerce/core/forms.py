from django import forms
from django.contrib.auth.models import User
from .models import Product, ProductImage, ProductReview, Address, ProductVariant
from django.forms import inlineformset_factory

INPUT = "w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 bg-white focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
TEXTAREA = "w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 bg-white focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent resize-none"
SELECT = "w-full border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-800 bg-white focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-transparent"
CHECKBOX = "w-4 h-4 accent-purple-500"
FILE = "w-full text-sm text-gray-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password")
        help_texts = {"username": ""}
        widgets = {
            "first_name": forms.TextInput(attrs={"class": INPUT}),
            "last_name": forms.TextInput(attrs={"class": INPUT}),
            "email": forms.EmailInput(attrs={"class": INPUT}),
            "username": forms.TextInput(attrs={"class": INPUT}),
            "password": forms.PasswordInput(attrs={"class": INPUT}),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": INPUT}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": INPUT}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT}),
            "price": forms.NumberInput(attrs={"class": INPUT}),
            "info": forms.Textarea(attrs={"class": TEXTAREA, "rows": 6}),
            "category": forms.Select(attrs={"class": SELECT}),
            "is_featured": forms.CheckboxInput(attrs={"class": CHECKBOX}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["variant", "image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": FILE}),
            "variant": forms.Select(attrs={"class": SELECT}),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields["variant"].queryset = ProductVariant.objects.filter(product=product)
        else:
            self.fields["variant"].queryset = ProductVariant.objects.none()

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,
    can_delete=True
)

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT}),
            "content": forms.Textarea(attrs={"class": TEXTAREA, "rows": 4}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["first_name", "last_name", "address_line_1", "address_line_2", "phone", "city", "state", "pincode"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": INPUT}),
            "last_name": forms.TextInput(attrs={"class": INPUT}),
            "address_line_1": forms.TextInput(attrs={"class": INPUT}),
            "address_line_2": forms.TextInput(attrs={"class": INPUT}),
            "phone": forms.TextInput(attrs={"class": INPUT}),
            "city": forms.TextInput(attrs={"class": INPUT}),
            "state": forms.TextInput(attrs={"class": INPUT}),
            "pincode": forms.TextInput(attrs={"class": INPUT}),
        }

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ["name", "price_adjustment", "stock", "is_available"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT}),
            "price_adjustment": forms.NumberInput(attrs={"class": INPUT}),
            "stock": forms.NumberInput(attrs={"class": INPUT}),
            "is_available": forms.CheckboxInput(attrs={"class": CHECKBOX}),
        }

ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    extra=3,
    can_delete=True,
    min_num=0,
    validate_min=False
)