import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from store.models import Category, Product


class Command(BaseCommand):
    help = "Create the production admin user and demo store data."

    def handle(self, *args, **options):
        User = get_user_model()

        # -------------------------
        # Create / update admin
        # -------------------------
        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        email = os.environ.get("DJANGO_ADMIN_EMAIL")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if username and email and password:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )

            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True

            if created:
                user.set_password(password)

            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' is ready."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Admin environment variables are missing. "
                    "Skipping admin creation."
                )
            )

        # -------------------------
        # Create categories
        # -------------------------
        categories = [
            (
                "Phones",
                "phones",
                "Powerful phones designed for everyday life.",
            ),
            (
                "Laptops",
                "laptops",
                "Fast, light and ready for work.",
            ),
            (
                "Tablets",
                "tablets",
                "Big ideas in a beautiful package.",
            ),
            (
                "Accessories",
                "accessories",
                "Small details that complete your setup.",
            ),
        ]

        category_objects = {}

        for name, slug, description in categories:
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": description,
                },
            )
            category_objects[slug] = category

        # -------------------------
        # Create demo products
        # -------------------------
        products = [
            (
                "Nova Phone Pro",
                "nova-phone-pro",
                "Pro performance in a compact design.",
                "A premium smartphone with a brilliant display, "
                "powerful processor and all-day battery.",
                79999,
                "phones",
            ),
            (
                "Nova Air 15",
                "nova-air-15",
                "Thin, fast and made for everyday work.",
                "A lightweight laptop with a crisp display "
                "and long battery life.",
                109999,
                "laptops",
            ),
            (
                "Nova Pad",
                "nova-pad",
                "Your ideas, anywhere.",
                "A versatile tablet for notes, entertainment "
                "and creative work.",
                59999,
                "tablets",
            ),
            (
                "Nova Buds",
                "nova-buds",
                "Immersive sound without the clutter.",
                "Wireless earbuds with a clean design "
                "and comfortable fit.",
                12999,
                "accessories",
            ),
        ]

        for name, slug, short, description, price, category_slug in products:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": category_objects[category_slug],
                    "name": name,
                    "short_description": short,
                    "description": description,
                    "price": price,
                    "stock": 20,
                    "is_featured": True,
                    "is_active": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo categories and products are ready."
            )
        )