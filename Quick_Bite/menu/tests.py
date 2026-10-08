from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductModelTests(TestCase):
    def test_product_can_be_created_with_valid_data(self):
        product = Product.objects.create(
            name='Classic Cheeseburger',
            image_url='https://example.com/cheeseburger.jpg',
            description='Juicy beef patty with cheddar.',
            price=Decimal('9.99'),
        )

        stored = Product.objects.get(pk=product.pk)

        self.assertEqual(stored.name, 'Classic Cheeseburger')
        self.assertEqual(stored.image_url, 'https://example.com/cheeseburger.jpg')
        self.assertEqual(stored.description, 'Juicy beef patty with cheddar.')
        self.assertEqual(stored.price, Decimal('9.99'))


class MenuPageTests(TestCase):
    def test_menu_page_returns_http_200(self):
        response = self.client.get(reverse('menu_list'))

        self.assertEqual(response.status_code, 200)

    def test_menu_page_displays_products_stored_in_the_database(self):
        Product.objects.create(
            name='French Fries',
            image_url='https://example.com/fries.jpg',
            description='Golden, crispy fries.',
            price=Decimal('3.99'),
        )
        Product.objects.create(
            name='Chicken Momo',
            image_url='https://example.com/momo.jpg',
            description='Steamed chicken dumplings.',
            price=Decimal('10.99'),
        )

        response = self.client.get(reverse('menu_list'))

        self.assertContains(response, 'French Fries')
        self.assertContains(response, 'Golden, crispy fries.')
        self.assertContains(response, '$3.99')
        self.assertContains(response, 'Chicken Momo')
        self.assertContains(response, 'Steamed chicken dumplings.')
        self.assertContains(response, '$10.99')

    def test_product_name_appears_in_the_rendered_page(self):
        Product.objects.create(
            name='Chocolate Milkshake',
            image_url='https://example.com/milkshake.jpg',
            description='Thick blended chocolate shake.',
            price=Decimal('7.49'),
        )

        response = self.client.get(reverse('menu_list'))

        self.assertContains(response, 'Chocolate Milkshake')


class AdminAuthenticationTests(TestCase):
    def test_django_admin_requires_authentication(self):
        response = self.client.get(reverse('admin:index'))

        self.assertRedirects(response, '/admin/login/?next=/admin/')
