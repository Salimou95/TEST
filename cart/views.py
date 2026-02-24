from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from store.models import Product
from .models import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """Ajoute ou met à jour un produit dans le panier."""
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id, available=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"], override_quantity=cd["override"])
        messages.success(request, f'"{product.name}" ajouté au panier.')
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """Supprime un produit du panier."""
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    cart.remove(product)
    messages.info(request, f'"{product.name}" retiré du panier.')
    return redirect("cart:cart_detail")


def cart_detail(request):
    """Affiche le contenu du panier."""
    cart = Cart(request)
    # Prépare un formulaire de mise à jour pour chaque article
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, "cart/cart_detail.html", {"cart": cart})
