"""Management command to populate the database with demo data."""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product


class Command(BaseCommand):
    help = "Populate the database with demo categories and products."

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            ("Électronique", "electronique"),
            ("Vêtements", "vetements"),
            ("Livres", "livres"),
            ("Sport", "sport"),
            ("Maison", "maison"),
        ]
        categories = {}
        for name, slug in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, slug=slug)
            categories[slug] = cat

        # Create products
        products_data = [
            ("Smartphone Galaxy X", "smartphone-galaxy-x", "electronique",
             "Dernier modèle avec écran AMOLED 6.7 pouces et triple caméra.", 699.99, 50),
            ("Laptop Pro 15", "laptop-pro-15", "electronique",
             "Ordinateur portable haute performance, 16 Go RAM, SSD 512 Go.", 1199.99, 20),
            ("Casque Bluetooth", "casque-bluetooth", "electronique",
             "Casque sans fil avec réduction de bruit active.", 149.99, 80),
            ("T-Shirt Premium", "t-shirt-premium", "vetements",
             "T-shirt en coton bio, disponible en plusieurs couleurs.", 29.99, 200),
            ("Jean Slim", "jean-slim", "vetements",
             "Jean coupe slim, confortable et résistant.", 59.99, 150),
            ("Veste Légère", "veste-legere", "vetements",
             "Veste légère imperméable, idéale pour le printemps.", 89.99, 60),
            ("Python pour les nuls", "python-pour-les-nuls", "livres",
             "Apprenez Python facilement avec ce guide pratique.", 24.99, 100),
            ("Django Web Development", "django-web-development", "livres",
             "Maîtrisez le développement web avec Django.", 34.99, 75),
            ("Raquette de Tennis", "raquette-tennis", "sport",
             "Raquette professionnelle pour joueurs confirmés.", 119.99, 30),
            ("Tapis de Yoga", "tapis-yoga", "sport",
             "Tapis antidérapant épaisseur 6mm, idéal pour le yoga et la méditation.", 39.99, 90),
            ("Cafetière Expresso", "cafetiere-expresso", "maison",
             "Machine à expresso avec broyeur intégré.", 249.99, 40),
            ("Lampe Design", "lampe-design", "maison",
             "Lampe de salon au design épuré, lumière LED réglable.", 79.99, 55),
        ]

        for name, slug, cat_slug, desc, price, stock in products_data:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": categories[cat_slug],
                    "description": desc,
                    "price": price,
                    "stock": stock,
                    "available": True,
                },
            )

        # Create superuser if it doesn't exist
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created (password: admin123)"))

        self.stdout.write(self.style.SUCCESS("Demo data loaded successfully!"))
