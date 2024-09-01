from django.db import models
from psqlextra.models import PostgresModel


class ProductSalesData(PostgresModel):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity_sold = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.product_name
