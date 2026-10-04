from django import forms
from store.models import Banner, Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category", "name", "slug", "short_description", "description",
            "price", "image", "stock", "is_featured", "is_active"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = [
            "title", "subtitle", "content", "image",
            "button_text", "button_url", "is_active", "sort_order"
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }
