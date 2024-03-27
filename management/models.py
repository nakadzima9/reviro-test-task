import uuid

from django.db import models


class Product(models.Model):
    identity_product = models.CharField(
        max_length=100, null=True, unique=True, default=uuid.uuid4,
        verbose_name="Unique identity of product"
    )
    title = models.CharField(max_length=150, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    price = models.PositiveIntegerField(verbose_name="Price")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    attachment = models.ForeignKey(
        'Company', on_delete=models.CASCADE, null=True,
        verbose_name='Attachment', default=None
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"UNIQUE_ID: {self.identity_product} - title: {self.title}"


class Company(models.Model):
    identity_company = models.CharField(
        max_length=100, null=True, unique=True, default=uuid.uuid4,
        verbose_name="Unique identity of company"
    )
    title = models.CharField(max_length=150, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    location = models.CharField(max_length=150, verbose_name="Location")
    schedule = models.CharField(max_length=50, verbose_name="Schedule of work")

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"UNIQUE_ID: {self.identity_company} - title: {self.title}"
