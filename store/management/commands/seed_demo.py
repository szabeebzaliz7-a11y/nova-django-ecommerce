from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = "Create demo categories and products without images."

    def handle(self, *args, **kwargs):
        data = [
            ("Phones", "phones", "Powerful phones designed for everyday life."),
            ("Laptops", "laptops", "Fast, light and ready for work."),
            ("Tablets", "tablets", "Big ideas in a beautiful package."),
            ("Accessories", "accessories", "Small details that complete your setup."),
        ]
        cats = {}
        for name, slug, desc in data:
            cats[slug], _ = Category.objects.get_or_create(
                slug=slug, defaults={"name": name, "description": desc}
            )

        products = [
            ("Nova Phone Pro", "nova-phone-pro", "Pro performance in a compact design.", "A premium smartphone with a brilliant display, powerful processor and all-day battery.", 79999, "phones"),
            ("Nova Air 15", "nova-air-15", "Thin, fast and made for everyday work.", "A lightweight laptop with a crisp display and long battery life.", 109999, "laptops"),
            ("Nova Pad", "nova-pad", "Your ideas, anywhere.", "A versatile tablet for notes, entertainment and creative work.", 59999, "tablets"),
            ("Nova Buds", "nova-buds", "Immersive sound without the clutter.", "Wireless earbuds with a clean design and comfortable fit.", 12999, "accessories"),
        ]
        for name, slug, short, desc, price, cat in products:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": cats[cat],
                    "name": name,
                    "short_description": short,
                    "description": desc,
                    "price": price,
                    "stock": 20,
                    "is_featured": True,
                    "is_active": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Demo data created."))
