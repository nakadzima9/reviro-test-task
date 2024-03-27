from rest_framework.pagination import LimitOffsetPagination


class CustomPaginator(LimitOffsetPagination):
    default_limit = 10


class ProductPaginator(CustomPaginator):
    limit_query_param = 'product_limit'
    offset_query_param = 'product_offset'
