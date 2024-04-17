import csv
from datetime import datetime

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import list, edit, UpdateView, View

from .forms import ProductForm, ProductUpdateForm
from .models import Product
from users.utils import PermissionDeniedView


class InventoryPermissionView(PermissionDeniedView):
    def has_permission(self, request):
        groups = request.user.groups.filter(name__in=['manager', 'employee'])
        return request.user.is_superuser or groups.exists()


class ProductListView(InventoryPermissionView, list.ListView):
    model = Product
    template_name = 'inventory/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('id')


class ProductCreateView(InventoryPermissionView, edit.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_create.html'
    success_url = reverse_lazy('inventory:product_list')

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs


class ProductEditView(InventoryPermissionView, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'inventory/product_edit.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('inventory:product_list')


class InventoryReportView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        products_in_inventory = Product.objects.all()

        if start_date and end_date:
            products_in_inventory = products_in_inventory.filter(
                created_at__range=[start_date, end_date]
            )

        # Generate filename for the CSV report
        today_date = datetime.now().strftime('%d-%m-%Y')
        filename = f"inventory_report_{today_date}.csv"

        # Create HTTP response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Write CSV header
        writer = csv.writer(response)
        writer.writerow(['Product ID', 'Name', 'Description', 'Price',
                         'Stock Quantity', 'created_at', 'updated_at'])

        for product in products_in_inventory:
            writer.writerow([product.id, product.name, product.description,
                             product.price, product.stock_quantity,
                             product.created_at, product.updated_at])

        return response
