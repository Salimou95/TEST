from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product


class StoreViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Cat", slug="test-cat")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            description="A test product.",
            price="19.99",
            stock=10,
        )

    def test_product_list_returns_200(self):
        response = self.client.get(reverse("store:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_product_list_by_category(self):
        response = self.client.get(
            reverse("store:product_list_by_category", args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_product_detail_returns_200(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_search(self):
        response = self.client.get(reverse("store:product_list") + "?q=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_search_no_result(self):
        response = self.client.get(reverse("store:product_list") + "?q=zzznoresult")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Product")
