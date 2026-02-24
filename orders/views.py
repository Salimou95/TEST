from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return redirect('orders:order_created', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_created.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})
