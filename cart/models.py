from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart:
    """Panier d'achat stocké en session."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # ------------------------------------------------------------------
    # Helpers privés
    # ------------------------------------------------------------------
    def _save(self):
        """Marque la session comme modifiée."""
        self.session.modified = True

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------
    def add(self, product, quantity=1, override_quantity=False):
        """Ajoute un produit ou met à jour sa quantité."""
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self._save()

    def remove(self, product):
        """Supprime un produit du panier."""
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self._save()

    def clear(self):
        """Vide complètement le panier."""
        del self.session[settings.CART_SESSION_ID]
        self._save()

    def __iter__(self):
        """Itère sur les articles du panier en enrichissant chaque ligne."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.pk)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Nombre total d'articles dans le panier."""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Prix total du panier."""
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
