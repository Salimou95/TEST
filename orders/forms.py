from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Formulaire de création de commande (informations de livraison)."""

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "city", "postal_code"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
        }
