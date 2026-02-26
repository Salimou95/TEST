from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
