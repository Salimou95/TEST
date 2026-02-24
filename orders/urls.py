from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("<int:order_id>/pay/", views.order_pay, name="order_pay"),
    path("history/", views.order_list, name="order_list"),
]
