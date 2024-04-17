from django.urls import path

from .views import (SaleCreateView, SalesListView, SaleDetailView,
                    SalesReportView, SalesReportFormView,
                    TopSoldProductsReportView)

app_name = 'sales'


urlpatterns = [
    path('crear/', SaleCreateView.as_view(), name='create'),
    path('lista/', SalesListView.as_view(), name='sales_list'),
    path('<uuid:uuid>/', SaleDetailView.as_view(), name='sale-detail'),
    path('reportes/', SalesReportFormView.as_view(),
         name='sales-report-form'),
    path('reporte-ventas/', SalesReportView.as_view(), name='sales-report'),
    path('reporte-top-ventas/', TopSoldProductsReportView.as_view(), name='top-sales-report'),
]