from django import forms


class CartAddProductForm(forms.Form):
    """Formulaire d'ajout au panier (quantité + option de remplacement)."""
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        label="Quantité",
        widget=forms.NumberInput(attrs={"class": "form-control", "style": "width:80px"}),
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
