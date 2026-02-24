from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        cat = Category.objects.create(name="Cat", slug="cat")
        self.product = Product.objects.create(
            category=cat, name="Item", slug="item", price="9.99", stock=5
        )

    def test_cart_detail_empty(self):
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertEqual(response.status_code, 200)

    def test_cart_add_redirects(self):
        response = self.client.post(
            reverse("cart:cart_add", args=[self.product.pk]),
            {"quantity": 1, "override": "False"},
        )
        self.assertRedirects(response, reverse("cart:cart_detail"))

    def test_cart_remove_redirects(self):
        # First add
        self.client.post(
            reverse("cart:cart_add", args=[self.product.pk]),
            {"quantity": 1, "override": "False"},
        )
        response = self.client.post(reverse("cart:cart_remove", args=[self.product.pk]))
        self.assertRedirects(response, reverse("cart:cart_detail"))
