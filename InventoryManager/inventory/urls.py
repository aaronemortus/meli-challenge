from django.urls import path

from .views import ProductListView, ProductCreateView, ProductEditView, \
    InventoryReportView

app_name = 'inventory'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('crear/', ProductCreateView.as_view(), name='product_create'),
    path('editar/<slug:slug>/', ProductEditView.as_view(), name='product_edit'),
    path('reporte-inventario/', InventoryReportView.as_view(),
         name='inventory-report'),

]