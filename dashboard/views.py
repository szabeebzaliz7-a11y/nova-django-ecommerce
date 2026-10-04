from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from store.models import Banner, Category, Product
from .forms import BannerForm, CategoryForm, ProductForm

User = get_user_model()


def staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="store:login",
    )(view_func)


@staff_required
def dashboard_home(request):
    context = {
        "product_count": Product.objects.count(),
        "active_product_count": Product.objects.filter(is_active=True).count(),
        "category_count": Category.objects.count(),
        "banner_count": Banner.objects.count(),
        "user_count": User.objects.count(),
        "recent_products": Product.objects.select_related("category")[:6],
    }
    return render(request, "dashboard/home.html", context)


@staff_required
def product_manage(request):
    products = Product.objects.select_related("category").all()
    return render(request, "dashboard/products.html", {"products": products})


@staff_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product created successfully.")
        return redirect("dashboard:products")
    return render(request, "dashboard/form.html", {"form": form, "title": "Add Product"})


@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect("dashboard:products")
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Product"})


@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("dashboard:products")
    return render(request, "dashboard/confirm_delete.html", {"object": product, "type": "product"})


@staff_required
def category_manage(request):
    categories = Category.objects.all()
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category created.")
        return redirect("dashboard:categories")
    return render(request, "dashboard/categories.html", {"categories": categories, "form": form})


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        try:
            category.delete()
            messages.success(request, "Category deleted.")
        except Exception:
            messages.error(request, "This category cannot be deleted while it has products.")
        return redirect("dashboard:categories")
    return render(request, "dashboard/confirm_delete.html", {"object": category, "type": "category"})


@staff_required
def banner_manage(request):
    banners = Banner.objects.all()
    return render(request, "dashboard/banners.html", {"banners": banners})


@staff_required
def banner_create(request):
    form = BannerForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Banner created successfully.")
        return redirect("dashboard:banners")
    return render(request, "dashboard/form.html", {"form": form, "title": "Add Banner"})


@staff_required
def banner_edit(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    form = BannerForm(request.POST or None, request.FILES or None, instance=banner)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Banner updated successfully.")
        return redirect("dashboard:banners")
    return render(request, "dashboard/form.html", {"form": form, "title": "Edit Banner"})


@staff_required
def banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == "POST":
        banner.delete()
        messages.success(request, "Banner deleted.")
        return redirect("dashboard:banners")
    return render(request, "dashboard/confirm_delete.html", {"object": banner, "type": "banner"})
