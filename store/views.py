from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, getattr(settings, 'PRODUCTS_PER_PAGE', 12))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
    })


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
    return render(request, 'store/product_detail.html', {'product': product})
