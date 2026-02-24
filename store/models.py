"""Models for the store app: Category and Product."""

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Product category (e.g. Electronics, Clothing)."""

    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_list_by_category", args=[self.slug])


class Product(models.Model):
    """A product available in the shop."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Catégorie",
    )
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Image",
    )
    available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.id, self.slug])

    @property
    def is_in_stock(self):
        """Return True if the product has stock available."""
        return self.stock > 0
