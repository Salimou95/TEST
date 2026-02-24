"""Models for the orders app: Order and OrderItem."""

from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    """An order placed by a user."""

    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente"),
        (STATUS_PROCESSING, "En cours"),
        (STATUS_SHIPPED, "Expédiée"),
        (STATUS_DELIVERED, "Livrée"),
        (STATUS_CANCELLED, "Annulée"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Utilisateur",
    )
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=250, verbose_name="Adresse")
    postal_code = models.CharField(max_length=20, verbose_name="Code postal")
    city = models.CharField(max_length=100, verbose_name="Ville")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name="Statut",
    )
    paid = models.BooleanField(default=False, verbose_name="Payée")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"

    def get_total_cost(self):
        """Return the total cost of all items in this order."""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """A single line item within an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Commande",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Produit",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prix unitaire"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """Return the total cost for this line item."""
        return self.price * self.quantity
