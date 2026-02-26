from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.middleware.csrf import get_token
from django.http import FileResponse, HttpResponse, JsonResponse
import os

# Store API URLs
from store.api_views import CategoryListAPIView, ProductListAPIView, ProductDetailAPIView

# Accounts API URLs
from accounts.api_views import RegisterAPIView, LoginAPIView, LogoutAPIView, CurrentUserAPIView, ProfileAPIView

# Cart API URLs
from cart.api_views import CartDetailAPIView, CartAddAPIView, CartRemoveAPIView

# Orders API URLs
from orders.api_views import OrderCreateAPIView, OrderHistoryAPIView, OrderDetailAPIView


def csrf_token_view(request):
    """Return a CSRF token so the React frontend can include it in requests."""
    return JsonResponse({'csrfToken': get_token(request)})


def serve_react(request):
    """Serve the React SPA index.html for all non-API routes."""
    index_file = os.path.join(settings.BASE_DIR, 'frontend', 'dist', 'index.html')
    if os.path.exists(index_file):
        return FileResponse(open(index_file, 'rb'), content_type='text/html')
    return HttpResponse(
        'React app not built. Run: cd frontend && npm run build',
        status=503,
    )


api_patterns = [
    # CSRF
    path('csrf/', csrf_token_view, name='api-csrf'),
    # Store
    path('categories/', CategoryListAPIView.as_view(), name='api-categories'),
    path('products/', ProductListAPIView.as_view(), name='api-products'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    # Auth
    path('auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('auth/user/', CurrentUserAPIView.as_view(), name='api-user'),
    path('auth/profile/', ProfileAPIView.as_view(), name='api-profile'),
    # Cart
    path('cart/', CartDetailAPIView.as_view(), name='api-cart'),
    path('cart/add/<int:product_id>/', CartAddAPIView.as_view(), name='api-cart-add'),
    path('cart/remove/<int:product_id>/', CartRemoveAPIView.as_view(), name='api-cart-remove'),
    # Orders
    path('orders/', OrderHistoryAPIView.as_view(), name='api-orders'),
    path('orders/checkout/', OrderCreateAPIView.as_view(), name='api-order-create'),
    path('orders/<int:order_id>/', OrderDetailAPIView.as_view(), name='api-order-detail'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    # Catch-all: serve the React SPA for any unmatched route
    re_path(r'^.*$', serve_react, name='react-app'),
]
