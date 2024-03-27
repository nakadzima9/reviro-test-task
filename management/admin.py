from django.contrib import admin
from management.models import Product, Company
# Register your models here.
admin.site.register([Product, Company])