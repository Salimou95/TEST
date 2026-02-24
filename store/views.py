from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Category, Product


def product_list(request, category_slug=None):
    """Liste des produits avec filtrage par catégorie et recherche."""
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Filtre par catégorie
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    # Barre de recherche
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query) | products.filter(
            description__icontains=query
        )

    # Pagination
    per_page = getattr(settings, "PRODUCTS_PER_PAGE", 8)
    paginator = Paginator(products, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "current_category": current_category,
        "page_obj": page_obj,
        "query": query,
    }
    return render(request, "store/product_list.html", context)


def product_detail(request, pk, slug):
    """Détail d'un produit."""
    product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
    return render(request, "store/product_detail.html", {"product": product})
