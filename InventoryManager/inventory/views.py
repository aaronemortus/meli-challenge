from django.urls import reverse_lazy
from django.views.generic import list, edit, UpdateView

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
