# myapp/tests.py
from django.test import TestCase
from django.urls import reverse
from custom_user.models import User
from product.models import Brand, Category, Product

class UserAdminViewTest(TestCase):
    def setUp(self):
        # Crear usuarios de prueba
        self.admin_user = User.objects.create_user(
            email='admin@admin.com',
            password='password123',
            is_staff=True,
        )

        self.normal_user = User.objects.create_user(
            email='user@user.com',
            password='password123',
            is_staff=False,
        )

        # Crear marcas, categorías y productos de prueba
        self.apple_brand = Brand.objects.create(name='Apple')
        self.samsung_brand = Brand.objects.create(name='Samsung')
        self.screen_category = Category.objects.create(name='Pantalla')
        self.battery_category = Category.objects.create(name='Batería')

        self.iphone_product = Product.objects.create(
            brand=self.apple_brand,
            category=self.screen_category,
            name='Reparación de pantalla IPhone 13',
            price=100,
            image='./item_images/iPhone.jpeg'
        )

        self.samsung_battery_product = Product.objects.create(
            brand=self.samsung_brand,
            category=self.battery_category,
            name='Reparación de batería Samsung A20',
            price=75,
            image='./item_images/Samsung.jpeg'
        )

    def test_staff_access_user_admin_view(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse('user_admin_view'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Lista de Usuarios')

    def test_non_staff_cannot_access_user_admin_view(self):
        self.client.force_login(self.normal_user)

        response = self.client.get(reverse('user_admin_view'), follow=True)  

        self.assertEqual(response.status_code, 200)  
        
        self.assertNotContains(response, 'Lista de Usuarios')
