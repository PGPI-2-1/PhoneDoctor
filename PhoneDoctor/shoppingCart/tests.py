# En tu archivo tests.py

from django.test import TestCase, Client
from django.urls import reverse
from custom_user.models import User
from product.models import Product, Category, Brand
from .models import CartItem

class CartItemModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')
    def test_cart_item_creation(self):
        user = User.objects.create(email='testuser@example.com', password='testpassword')
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category)
        cart_item = CartItem.objects.create(user=user, product=product, quantity=2, is_processed=False)

        self.assertEqual(cart_item.user, user)
        self.assertEqual(cart_item.product, product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertFalse(cart_item.is_processed)

class CartItemViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')
        self.product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=10)
    def test_add_to_cart_quantity_exceeded(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        self.client.login(email='testuser@example.com', password='testpassword')

        response = self.client.get(reverse('add_to_cart', args=[product.id]), {'cantidad': 10})

        cart_item = CartItem.objects.filter(user=self.user, product=product).first()
        self.assertIsNone(cart_item)

    def test_add_to_cart_quantity_zero(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=10)
        self.client.login(email='testuser@example.com', password='testpassword')

        response = self.client.get(reverse('add_to_cart', args=[product.id]), {'cantidad': 0})

        cart_item = CartItem.objects.filter(user=self.user, product=product).first()
        self.assertIsNone(cart_item)

    def test_add_to_cart_authenticated_user(self):
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]), {'cantidad': 3})
        self.assertEqual(response.status_code, 302)

        cart_item = CartItem.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 3)

    def test_add_to_cart_unauthenticated_user(self):

        response = self.client.get(reverse('add_to_cart', args=[self.product.id]), {'cantidad': 2})
        self.assertEqual(response.status_code, 302)

        cart_item = CartItem.objects.get(user=None, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    
