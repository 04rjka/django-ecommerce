from django import forms
from django.contrib.auth.models import User
from .models import Product,ProductImage,ProductReview,Address,ProductVariant
from django.forms import inlineformset_factory

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name","last_name","email","username","password")
        help_texts = {
            "username":""
        }
        widgets = {
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password": forms.PasswordInput(attrs={"class":"form-control"})
        }
        
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class":"form-control"}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class":"form-control"}
    ))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        widgets = {
            "name" : forms.TextInput(attrs={"class":"form-control"}),
            "price" : forms.NumberInput(attrs={"class":"form-control"}),
            "info" : forms.Textarea(attrs={"class":"form-control","rows":8}),
            "category" : forms.Select(attrs={"class":"form-select"}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = "__all__"

        widgets = {
            "image" : forms.FileInput(attrs={"class":"form-control"}),
        }
    def __init__(self,*args,**kwargs):
        product = kwargs.pop("product",None)
        super().__init__(*args,**kwargs)

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
        fields = ["title","content"]

        widgets = {
            "title" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "content" : forms.Textarea(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white","rows":4})
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["first_name","last_name","address_line_1","address_line_2","phone","city","state","pincode"]

        widgets = {
            "first_name" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "last_name" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "address_line_1" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "address_line_2" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "phone" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "city" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "state" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
            "pincode" : forms.TextInput(attrs={"class":"border w-full rounded px-2 py-1 border-gray-300 bg-white"}),
        }

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ["name", "price_adjustment", "stock", "is_available"]
        widgets = {
            "name":             forms.TextInput(attrs={"class": "form-control"}),
            "price_adjustment": forms.NumberInput(attrs={"class": "form-control"}),
            "stock":            forms.NumberInput(attrs={"class": "form-control"}),
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