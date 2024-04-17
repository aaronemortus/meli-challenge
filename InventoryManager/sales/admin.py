from django.contrib import admin

from .models import Sale, SaleItem


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'sale_date', 'total',)


@admin.register(SaleItem)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity_sold',)
