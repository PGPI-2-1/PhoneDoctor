from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Brand, Product

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email='email@email.com', password='useruser', is_staff=True, is_superuser=True)
        self.client.login(email='email@email.com', password='useruser')
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')

    def test_new_category(self):
        response = self.client.get(reverse('new_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/form.html')

    def test_new_brand(self):
        response = self.client.get(reverse('new_brand'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/form.html')

    def test_new_product_staff_user(self):
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/form.html')

        data = {'name': 'Test Product', 'price': 10.0, 'brand': Brand.objects.create(name='New Brand').id,
                'category': Category.objects.create(name='New Category').id, 'quantity': 5,'image': 'path/to/test/image.jpg'}
        response = self.client.post(reverse('new'), data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Product.objects.filter(name='Test Product').exists())
    
    def test_new_product_non_staff_user(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 403)
    
    def test_new_product_invalid_form(self):
        response = self.client.get(reverse('new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/form.html')

        data = {'name': '', 'price': -10.0, 'brand': Brand.objects.create(name='New Brand').id,
                'category': Category.objects.create(name='New Category').id, 'quantity': -5,'image': 'path/to/test/image.jpg'}
        response = self.client.post(reverse('new'), data)
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(Product.objects.filter(name='Test Product').exists())

    def test_delete_product_staff_user(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category)
        response = self.client.post(reverse('delete', args=[product.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_product_non_staff_user(self):
        self.user.is_staff = False
        self.user.save()
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category)
        response = self.client.post(reverse('delete', args=[product.id]))
        self.assertEqual(response.status_code, 403)

    def test_edit_product(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category)
        response = self.client.get(reverse('edit', args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/form.html')

    def test_product_info(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category)
        product.image = 'path/to/test/image.jpg'  # Asigna una ruta de imagen ficticia
        product.save()

        response = self.client.get(reverse('product_info', args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/info.html')

    def test_edit_product_post(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category)
        data = {'name': 'Updated Product','description':'Description update test' ,'price': 15.0, 'brand': self.brand.id, 'category': self.category.id, 'quantity': 5,'image': 'path/to/test/image.jpg'}
        response = self.client.post(reverse('edit', args=[product.id]), data)
        self.assertEqual(response.status_code, 302)


        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.price, 15.0)
        self.assertEqual(updated_product.brand, self.brand)
        self.assertEqual(updated_product.category, self.category)
        self.assertEqual(updated_product.quantity, 5)

