from rest_framework import serializers

from management.models import Product, Company
from management.paginators import ProductPaginator


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'identity_product',
            'title',
            'description',
            'price',
            'quantity',
            'attachment',
        ]


class ProductSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'quantity',
            'attachment',
        ]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'identity_company',
            'title',
            'description',
            'location',
            'schedule',
        ]


class CompanyDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_paginated_products')

    class Meta:
        model = Company
        fields = [
            'id',
            'identity_company',
            'title',
            'description',
            'location',
            'schedule',
            'products',
        ]

    def get_paginated_products(self, obj):
        request = self.context['request']
        products = obj.product_set.all()
        paginator = ProductPaginator()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return serializer.data


class CompanySchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'title',
            'description',
            'location',
            'schedule',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    attachment = CompanySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'identity_product',
            'title',
            'description',
            'price',
            'quantity',
            'attachment',
        ]
