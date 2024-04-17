from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name='Producto 1',
            description='Descripción del producto 1',
            price=10.0,
            stock_quantity=50
        )
        self.product2 = Product.objects.create(
            name='Producto 2',
            description='Descripción del producto 2',
            price=15.0,
            stock_quantity=30
        )

    def test_product_creation(self):
        self.assertEqual(self.product1.name, 'Producto 1')
        self.assertEqual(self.product2.description, 'Descripción del producto 2')
        self.assertEqual(self.product1.price, 10.0)
        self.assertEqual(self.product2.stock_quantity, 30)

    def test_product_list_view(self):
        url = reverse('inventory:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        url = reverse('inventory:product_detail', kwargs={'slug': self.product1.slug})
        response = self.client.get(url)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.description)
        self.assertContains(response, self.product1.price)
        self.assertContains(response, self.product1.stock_quantity)

    def test_product_update(self):
        new_quantity = 20
        url = reverse('inventory:product_update', kwargs={'slug': self.product1.slug})
        data = {'stock_quantity': new_quantity}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_product = Product.objects.get(pk=self.product1.pk)
        self.assertEqual(updated_product.stock_quantity, new_quantity)
