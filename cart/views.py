"""Views for the cart app."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    """Display the shopping cart with all items and the total price."""
    cart = Cart(request)
    # Attach the update form to each item
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, "cart/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    """Add a product to the cart or update its quantity."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )
        messages.success(request, f'"{product.name}" a été ajouté au panier.')
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """Remove a product from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'"{product.name}" a été retiré du panier.')
    return redirect("cart:cart_detail")
