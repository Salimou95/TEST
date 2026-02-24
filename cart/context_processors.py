"""Context processors for the cart app."""

from .cart import Cart


def cart_item_count(request):
    """Inject the cart item count into every template context."""
    return {"cart_item_count": len(Cart(request))}
