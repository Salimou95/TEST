"""Forms for the cart app."""

from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Form to add a product to the cart or update its quantity."""

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label="Quantité",
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )
