from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """Formulaire d'inscription avec email obligatoire."""
    email = forms.EmailField(required=True, label="Adresse e-mail")
    first_name = forms.CharField(max_length=30, required=False, label="Prénom")
    last_name = forms.CharField(max_length=150, required=False, label="Nom")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Crée automatiquement le profil lié
            UserProfile.objects.get_or_create(user=user)
        return user


class UserUpdateForm(forms.ModelForm):
    """Mise à jour des informations de base de l'utilisateur."""
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    """Mise à jour du profil étendu."""

    class Meta:
        model = UserProfile
        fields = ["phone", "address", "city", "postal_code"]
