from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm
from .models import Banner, Category, Product


def home(request):
    banners = Banner.objects.filter(is_active=True)
    featured = Product.objects.filter(
        is_active=True, is_featured=True
    ).select_related("category")[:8]
    categories = Category.objects.all()[:6]
    return render(
        request,
        "store/home.html",
        {
            "banners": banners,
            "featured_products": featured,
            "categories": categories,
        },
    )


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related("category")
    categories = Category.objects.all()
    selected_category = request.GET.get("category", "")
    query = request.GET.get("q", "")

    if selected_category:
        products = products.filter(category__slug=selected_category)
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    return render(
        request,
        "store/product_list.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": selected_category,
            "query": query,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
    )
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]
    return render(
        request,
        "store/product_detail.html",
        {"product": product, "related": related},
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("store:home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("store:account")
    return render(request, "store/auth.html", {"form": form, "mode": "register"})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("store:home")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user:
            login(request, user)
            messages.success(request, "Welcome back.")
            return redirect(request.GET.get("next") or "store:home")
        form.add_error(None, "Invalid username or password.")
    return render(request, "store/auth.html", {"form": form, "mode": "login"})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("store:home")


@login_required
def account(request):
    return render(request, "store/account.html")


@login_required
def cart(request):
    cart_ids = request.session.get("cart", [])
    products = Product.objects.filter(id__in=cart_ids, is_active=True)
    return render(request, "store/cart.html", {"products": products})


def add_to_cart(request, pk):
    if request.method != "POST":
        return redirect("store:product_list")
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart_ids = request.session.get("cart", [])
    if product.pk not in cart_ids:
        cart_ids.append(product.pk)
    request.session["cart"] = cart_ids
    messages.success(request, f"{product.name} was added to your bag.")
    return redirect(request.POST.get("next") or product.get_absolute_url())


def remove_from_cart(request, pk):
    cart_ids = request.session.get("cart", [])
    if pk in cart_ids:
        cart_ids.remove(pk)
    request.session["cart"] = cart_ids
    return redirect("store:cart")
