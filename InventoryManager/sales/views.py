import csv
from datetime import datetime

from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import FormView, View, DetailView, TemplateView, list
from django.contrib import messages

from .models import Product, Sale, SaleItem
from .forms import SaleForm, SalesReportForm
from users.utils import PermissionDeniedView


class SalesPermissionView(PermissionDeniedView):
    def has_permission(self, request):
        groups = request.user.groups.filter(name__in=['manager', 'employee'])
        return request.user.is_superuser or groups.exists()


class CustomerPermissionView(PermissionDeniedView):
    def has_permission(self, request):
        return request.user.is_authenticated


class SaleCreateView(SalesPermissionView, FormView):
    template_name = 'sales/sale_create.html'
    form_class = SaleForm
    success_url = '/sales/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

    def form_valid(self, form):
        sale = form.save(commit=False)

        # Calculate total sale
        total_sale = 0
        products_selected = self.request.POST.getlist('products')
        for product_id in products_selected:
            product = Product.objects.get(pk=product_id)
            quantity_sold = int(self.request.POST.get(f'quantity_{product_id}', 0))
            total_sale += product.price * quantity_sold
        sale.total = total_sale
        sale.save()

        # Create Sale items
        try:
            for product_id in products_selected:
                product = Product.objects.get(pk=product_id)
                quantity_sold = int(
                    self.request.POST.get(f'quantity_{product_id}', 0))
                sale.sale_items.create(product=product,
                                       quantity_sold=quantity_sold)
                # Updating stock
                product.stock_quantity -= quantity_sold
                product.save()
        except IntegrityError as e:
            error_message = (f'Lo sentimos, no hay suficiente stock disponible'
                             f' para el producto "{product.name}". No fue'
                             f' posible agregarlo a la compra.')
            messages.error(self.request, error_message)

        self.sale = sale
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al usuario a la vista de detalle de la venta recién creada
        return reverse_lazy('sales:sale-detail', kwargs={'uuid': self.sale.id})


class SalesListView(CustomerPermissionView, list.ListView):
    model = Sale
    template_name = 'sales/sales_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        groups = user.groups.all()
        if groups.filter(name='customer').exists():
            queryset = queryset.filter(customer=user)
        return queryset.order_by('id')


class SaleDetailView(CustomerPermissionView, DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'

    def get_object(self, queryset=None):
        return Sale.objects.get(id=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = messages.get_messages(self.request)
        return context


class SalesReportFormView(SalesPermissionView, TemplateView):
    template_name = 'sales/sales_report_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SalesReportForm()
        context['top_sales_form'] = SalesReportForm()
        return context


class SalesReportView(SalesPermissionView, View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        # Filter sales with start_date and end_date
        sales = Sale.objects.filter(sale_date__range=[start_date, end_date])

        today_date = datetime.now().strftime('%d-%m-%Y')
        filename = f"sales_report_{today_date}.csv"

        # Create response HTTP with the CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Write header
        writer = csv.writer(response)
        writer.writerow(['Venta ID', 'Cliente', 'Fecha de venta', 'Producto',
                         'Cantidad vendida', 'Precio unitario',
                         'Total por producto'])

        for sale in sales:
            sale_items = sale.sale_items.all()
            for sale_item in sale_items:
                writer.writerow([sale.id, sale.customer.username, sale.sale_date,
                                  sale_item.product.name, sale_item.quantity_sold,
                                  sale_item.product.price, sale_item.total_price])

        return response


class TopSoldProductsReportView(SalesPermissionView, View):
    def get(self, request, *args, **kwargs):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Convertir las cadenas de fecha en objetos de fecha
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        # Consultar los productos más vendidos en el rango de fechas especificado
        top_sold_products = SaleItem.objects.filter(
            sale__sale_date__range=(start_date, end_date)
        ).values('product__name').annotate(
            total_sold=Sum('quantity_sold')
        ).order_by('-total_sold')[:10]

        today_date = datetime.now().strftime('%d-%m-%Y')
        filename = f"top_sold_products_report_{today_date}.csv"

        # Crear el archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Escribir los datos en el archivo CSV
        writer = csv.writer(response)
        writer.writerow(['Producto', 'Cantidad Vendida'])
        for product in top_sold_products:
            writer.writerow([product['product__name'], product['total_sold']])

        return response
