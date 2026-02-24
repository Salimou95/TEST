"""Views for the store app: product list and product detail."""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q

from .models import Category, Product


def product_list(request, category_slug=None):
    """Display the list of available products with optional filtering and search."""
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Filter by category
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    # Search by name or description
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Pagination
    per_page = getattr(settings, "PRODUCTS_PER_PAGE", 9)
    paginator = Paginator(products, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "store/product_list.html",
        {
            "categories": categories,
            "current_category": current_category,
            "products": page_obj,
            "query": query,
        },
    )


def product_detail(request, pk, slug):
    """Display a single product detail page."""
    product = get_object_or_404(Product, id=pk, slug=slug, available=True)
    return render(request, "store/product_detail.html", {"product": product})
