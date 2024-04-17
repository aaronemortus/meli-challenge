import uuid
from django.db import models
from django.core.exceptions import ValidationError

from users.models import CustomUser
from inventory.models import Product


class Sale(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta #{self.id} "


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE,
                             related_name='sale_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()

    def clean(self):
        if self.quantity_sold > self.product.stock_quantity:
            raise ValidationError('No hay suficiente stock '
                                  'disponible para este producto')
