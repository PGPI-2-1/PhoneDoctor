# orders/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from product.models import Product, Category, Brand
from shoppingCart.models import CartItem
from .models import Order

class OrderModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='testpassword')

    def test_order_creation(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=self.user, product=product, quantity=2, is_processed=False)
        
        order = Order.objects.create(user=self.user, address='Test Address', email='test@example.com', status=Order.StatusChoices.PAGADO, precio_total=20.0)
        order.items.add(cart_item)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.address, 'Test Address')
        self.assertEqual(order.email, 'test@example.com')
        self.assertEqual(order.status, Order.StatusChoices.PAGADO)
        self.assertEqual(order.precio_total, 20.0)
        self.assertEqual(order.items.count(), 1)

class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')

    def test_checkout_authenticated_user(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=self.user, product=product, quantity=2, is_processed=False)
        
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.post(reverse('checkout'), {'address': 'Test Address'})
        
        self.assertEqual(response.status_code, 302) 

        order = Order.objects.get(user=self.user)
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(all(cart_item.is_processed for cart_item in CartItem.objects.filter(user=self.user)))

    def test_checkout_unauthenticated_user(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=None, product=product, quantity=2, is_processed=False)

        response = self.client.post(reverse('checkout'), {'address': 'Test Address', 'email': 'test@example.com'})
        
        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(user=None)
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(all(cart_item.is_processed for cart_item in CartItem.objects.filter(user=None)))
