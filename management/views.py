from django.http import Http404
from django.core.paginator import Paginator

from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from management.models import Product, Company
from management.serializers import (
    ProductSerializer,
    ProductSchemaSerializer,
    ProductDetailSerializer,
    CompanySerializer,
    CompanySchemaSerializer,
    CompanyDetailSerializer,
)

from management.paginators import CustomPaginator


class ProductList(APIView):
    """
    List all products of the company
    """

    @extend_schema(
        responses=ProductSerializer,
        parameters=[
            OpenApiParameter(name='offset',
                             location=OpenApiParameter.QUERY,
                             description='offset for products pagination',
                             required=False,
                             type=int
                             )
            , OpenApiParameter(name='limit',
                               location=OpenApiParameter.QUERY,
                               description='records limit for products pagination',
                               required=False,
                               type=int
                               )
        ],
        summary="Get all products."
    )
    def get(self, request):
        products = Product.objects.all()
        paginator = CustomPaginator()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductDetailSerializer(paginated_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ProductSchemaSerializer,
        responses=ProductDetailSerializer,
        summary="Create product."
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            company_pk = serializer.data.get('attachment')
            company = Company.objects.get(id=company_pk)
            company_serializer = CompanySerializer(company)
            result = dict()
            result.update(serializer.data)
            result['attachment'] = company_serializer.data
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    """
    Retrieve, update and delete a product instance.
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    @extend_schema(
        responses=ProductSerializer,
        summary="Get product by ID."
    )
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    @extend_schema(
        request=ProductSchemaSerializer,
        responses=ProductSerializer,
        summary="Update product by ID."
    )
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ProductSchemaSerializer,
        responses=ProductDetailSerializer,
        summary="Partial update product by ID."
    )
    def patch(self, request, pk):
        product = self.get_object(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete product by ID."
    )
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyList(APIView):
    """
    List all the companies
    """

    @extend_schema(
        responses=CompanySerializer,
        parameters=[
            OpenApiParameter(name='offset',
                             location=OpenApiParameter.QUERY,
                             description='offset for companies pagination',
                             required=False,
                             type=int
                             )
            , OpenApiParameter(name='limit',
                               location=OpenApiParameter.QUERY,
                               description='records limit for companies pagination',
                               required=False,
                               type=int
                               )
        ],
        summary="Get all companies."
    )
    def get(self, request):
        companies = Company.objects.all()
        paginator = CustomPaginator()
        paginated_companies = paginator.paginate_queryset(companies, request)
        serializer = CompanyDetailSerializer(paginated_companies, context={'request': request}, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=CompanySchemaSerializer,
        responses=CompanySerializer,
        summary="Create company."
    )
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetail(APIView):
    """
    Retrieve, update and delete a company instance.
    """

    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    @extend_schema(
        responses=CompanyDetailSerializer,
        parameters=[
            OpenApiParameter(name='product_offset',
                             location=OpenApiParameter.QUERY,
                             description='offset for products field pagination',
                             required=False,
                             type=int
                             )
            , OpenApiParameter(name='product_limit',
                               location=OpenApiParameter.QUERY,
                               description='records limit for products field pagination',
                               required=False,
                               type=int
                               )
        ],
        summary="Get company by ID."
    )
    def get(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanyDetailSerializer(company, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        request=CompanySchemaSerializer,
        responses=CompanySerializer,
        summary="Update company by ID."
    )
    def put(self, request, pk):
        company = self.get_object(pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CompanySchemaSerializer,
        responses=CompanySerializer,
        summary="Partial update company by ID."
    )
    def patch(self, request, pk):
        company = self.get_object(pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete company by ID."
    )
    def delete(self, request, pk):
        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
