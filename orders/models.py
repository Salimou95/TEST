from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    """Commande passée par un utilisateur."""

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("processing", "En cours"),
        ("shipped", "Expédiée"),
        ("delivered", "Livrée"),
        ("cancelled", "Annulée"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", verbose_name="Utilisateur"
    )
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    email = models.EmailField(verbose_name="E-mail")
    address = models.TextField(verbose_name="Adresse de livraison")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Statut"
    )
    paid = models.BooleanField(default=False, verbose_name="Payée")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created"]

    def __str__(self):
        return f"Commande #{self.pk}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Ligne de commande (produit + quantité + prix unitaire)."""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Commande"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items", verbose_name="Produit"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity
