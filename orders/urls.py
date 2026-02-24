"""URL patterns for the orders app."""

from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("payment/<int:order_id>/", views.payment_process, name="payment_process"),
    path("detail/<int:order_id>/", views.order_detail, name="order_detail"),
    path("my-orders/", views.order_list, name="order_list"),
]
