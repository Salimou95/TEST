from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    """Création de la commande à partir du contenu du panier."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Votre panier est vide.")
        return redirect("store:product_list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # Crée les lignes de commande
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # Vide le panier
            cart.clear()
            messages.success(request, f"Commande #{order.pk} passée avec succès !")
            return redirect("orders:order_detail", order_id=order.pk)
    else:
        # Pré-remplit avec les données du profil si disponible
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }
        if hasattr(request.user, "profile"):
            profile = request.user.profile
            initial.update({
                "address": profile.address,
                "city": profile.city,
                "postal_code": profile.postal_code,
            })
        form = OrderCreateForm(initial=initial)

    return render(request, "orders/order_create.html", {"cart": cart, "form": form})


@login_required
def order_detail(request, order_id):
    """Récapitulatif et simulation de paiement d'une commande."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_pay(request, order_id):
    """Simulation du paiement d'une commande."""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if request.method == "POST" and not order.paid:
        order.paid = True
        order.status = "processing"
        order.save()
        messages.success(request, f"Paiement simulé avec succès pour la commande #{order.pk} !")
    return redirect("orders:order_detail", order_id=order.pk)


@login_required
def order_list(request):
    """Historique des commandes de l'utilisateur connecté."""
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})
