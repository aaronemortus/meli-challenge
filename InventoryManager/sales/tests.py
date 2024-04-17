from django.test import TestCase
from django.urls import reverse

from .models import Sale, SaleItem
from users.models import CustomUser
from inventory.models import Product


class SaleTestCase(TestCase):
    def setUp(self):
        self.customer = CustomUser.objects.create(
            username='test_customer',
            email='customer@example.com'
        )
        self.product = Product.objects.create(
            name='Producto de prueba',
            description='Descripción del producto',
            price=10.0,
            stock_quantity=50
        )
        self.sale = Sale.objects.create(customer=self.customer, total=20.0)

    def test_sale_creation(self):
        self.assertEqual(self.sale.customer, self.customer)
        self.assertEqual(self.sale.total, 20.0)

    def test_sale_item_creation(self):
        sale_item = SaleItem.objects.create(sale=self.sale, product=self.product, quantity_sold=2)
        self.assertEqual(sale_item.sale, self.sale)
        self.assertEqual(sale_item.product, self.product)
        self.assertEqual(sale_item.quantity_sold, 2)

    def test_sale_list_view(self):
        url = reverse('sales:sales_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sale_detail_view(self):
        url = reverse('sales:sale-detail', kwargs={'uuid': self.sale.id})
        response = self.client.get(url)
        self.assertContains(response, self.customer.username)
        self.assertContains(response, self.sale.total)

    def test_sale_create_view(self):
        url = reverse('sales:create')
        data = {'customer': self.customer.id, 'total': 25.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Sale.objects.filter(total=25.0).exists())
