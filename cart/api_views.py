from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from store.models import Product
from .cart import Cart


class CartDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = Cart(request)
        items = []
        for item in cart:
            items.append({
                'product_id': item['product'].id,
                'product_name': item['product'].name,
                'product_slug': item['product'].slug,
                'product_image': request.build_absolute_uri(item['product'].image.url) if item['product'].image else None,
                'price': item['price'],
                'quantity': item['quantity'],
                'total_price': item['total_price'],
            })
        return Response({
            'items': items,
            'total_price': cart.get_total_price(),
            'total_items': len(cart),
        })


class CartAddAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.data.get('quantity', 1))
        override = request.data.get('override_quantity', False)
        cart.add(product=product, quantity=quantity, override_quantity=override)
        return Response({'detail': 'Product added to cart.'})


class CartRemoveAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return Response({'detail': 'Product removed from cart.'})
