from .models import Cart


def cart_count(request):
    """Injecte le nombre d'articles du panier dans tous les templates."""
    return {"cart_count": len(Cart(request))}
