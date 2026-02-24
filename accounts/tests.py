from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class AccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123", email="test@example.com"
        )
        UserProfile.objects.get_or_create(user=self.user)

    def test_register_get(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(response, "/accounts/login/?next=/accounts/profile/")

    def test_profile_accessible_when_logged_in(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass456!",
            "password2": "StrongPass456!",
        })
        self.assertTrue(User.objects.filter(username="newuser").exists())
