"""Admin configuration for the orders app."""

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "first_name", "last_name", "status", "paid", "created_at"]
    list_filter = ["paid", "status", "created_at"]
    search_fields = ["user__username", "first_name", "last_name", "email"]
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]
