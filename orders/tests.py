from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product
from .models import Order, OrderItem


class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="buyer", password="pass1234!")
        cat = Category.objects.create(name="Cat", slug="catorder")
        self.product = Product.objects.create(
            category=cat, name="Widget", slug="widget", price="15.00", stock=10
        )

    def test_order_create_requires_login(self):
        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 302)

    def test_order_list_requires_login(self):
        response = self.client.get(reverse("orders:order_list"))
        self.assertEqual(response.status_code, 302)

    def test_order_create_with_cart(self):
        self.client.login(username="buyer", password="pass1234!")
        # Add item to cart
        self.client.post(
            reverse("cart:cart_add", args=[self.product.pk]),
            {"quantity": 2, "override": "False"},
        )
        response = self.client.post(reverse("orders:order_create"), {
            "first_name": "Alice",
            "last_name": "Martin",
            "email": "alice@example.com",
            "address": "1 rue Test",
            "city": "Lyon",
            "postal_code": "69000",
        })
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.items.count(), 1)
        self.assertRedirects(response, reverse("orders:order_detail", args=[order.pk]))

    def test_payment_simulation(self):
        self.client.login(username="buyer", password="pass1234!")
        order = Order.objects.create(
            user=self.user,
            first_name="Alice", last_name="Martin",
            email="alice@example.com",
            address="1 rue Test", city="Lyon", postal_code="69000",
        )
        self.assertFalse(order.paid)
        self.client.post(reverse("orders:order_pay", args=[order.pk]))
        order.refresh_from_db()
        self.assertTrue(order.paid)
