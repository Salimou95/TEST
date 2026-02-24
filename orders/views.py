"""Views for the orders app."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    """Display the order form and create the order on POST."""
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
            # Create order items from cart contents
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # Clear the cart after order creation
            cart.clear()
            messages.success(
                request,
                "Votre commande a été passée avec succès ! Procédez au paiement.",
            )
            return redirect("orders:payment_process", order_id=order.id)
    else:
        # Pre-fill email from user profile
        form = OrderCreateForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        )

    return render(
        request,
        "orders/order_create.html",
        {"cart": cart, "form": form},
    )


@login_required
def payment_process(request, order_id):
    """Simulate a payment process page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        # Simulate successful payment
        order.paid = True
        order.status = Order.STATUS_PROCESSING
        order.save()
        messages.success(request, "Paiement simulé avec succès !")
        return redirect("orders:order_detail", order_id=order.id)
    return render(request, "orders/payment.html", {"order": order})


@login_required
def order_detail(request, order_id):
    """Display the detail of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_list(request):
    """Display all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})
