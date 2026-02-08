from django import forms
from django.contrib.auth.models import User
from .models import Product,ProductImage
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

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = "__all__"

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,
    can_delete=True
)