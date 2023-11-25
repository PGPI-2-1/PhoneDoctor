from django.test import TestCase
from custom_user.models import User
from product.models import Brand, Category, Product
from django.urls import reverse

class IndexViewTest(TestCase):
    def setUp(self):
        
        self.admin_user = User.objects.create_user(
            email='admin@admin.com',
            password='password123',
            is_superuser=True,
            is_staff=True
        )
        
        self.normal_user = User.objects.create_user(
            email='user@user.com',
            password='password456',
        )

        # Crear marcas y categorías de prueba
        self.apple_brand = Brand.objects.create(name='Apple')
        self.samsung_brand = Brand.objects.create(name='Samsung')
        self.screen_category = Category.objects.create(name='Pantalla')
        self.battery_category = Category.objects.create(name='Batería')

        # Crear productos de prueba
        self.iphone_product = Product.objects.create(
            brand=self.apple_brand,
            category=self.screen_category,
            name='Reparación de pantalla IPhone 13',
            price=100,
            image='./item_images/iPhone.jpeg'
        )

        self.samsung_product = Product.objects.create(
            brand=self.samsung_brand,
            category=self.battery_category,
            name='Reparación de bateria Samsung A20',
            price=75,
            image='./item_images/Samsung.jpeg'
        )

    def test_products_displayed_when_filtering(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Samsung')
        self.assertContains(response, 'Pantalla')
        self.assertContains(response, 'Batería')

        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertContains(response, 'Reparación de bateria Samsung A20')

        response = self.client.get(reverse('index'), {'category': 'Pantalla'})
        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertNotContains(response, 'Reparación de bateria Samsung A20')

    def test_no_products_displayed_when_filtering_no_match(self):
        self.client.login(email='user@user.com', password='password123')

        response = self.client.get(reverse('index'), {'category': 'Batería'})

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, 'Reparación de pantalla IPhone 13')

    def test_products_displayed_when_searching(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Samsung')
        self.assertContains(response, 'Pantalla')
        self.assertContains(response, 'Batería')

        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertContains(response, 'Reparación de bateria Samsung A20')

        response = self.client.get(reverse('index'), {'q': 'Pantalla'})
        self.assertContains(response, 'Reparación de pantalla IPhone 13')

    def test_no_products_displayed_when_searching(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Samsung')
        self.assertContains(response, 'Pantalla')
        self.assertContains(response, 'Batería')

        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertContains(response, 'Reparación de bateria Samsung A20')

        response = self.client.get(reverse('index'), {'q': 'huawei'})
        self.assertNotContains(response, 'Reparación de pantalla IPhone 13')
        self.assertNotContains(response, 'Reparación de bateria Samsung A20')

    def test_category_brand_query_filter(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Samsung')
        self.assertContains(response, 'Pantalla')
        self.assertContains(response, 'Batería')

        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertContains(response, 'Reparación de bateria Samsung A20')

        response = self.client.get(reverse('index'), {'category': 'Pantalla', 'brand': 'Apple', 'q': 'IPhone'})
        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertNotContains(response, 'Reparación de batería Samsung A20')

    def test_category_brand_filter(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'), {'category': 'Pantalla', 'brand': 'Apple'})
        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertNotContains(response, 'Reparación de batería Samsung A20')

    def test_category_query_filter(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'), {'category': 'Pantalla', 'q': 'IPhone'})
        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertNotContains(response, 'Reparación de batería Samsung A20')

    def test_brand_query_filter(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'), {'brand': 'Apple', 'q': 'IPhone'})
        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertNotContains(response, 'Reparación de batería Samsung A20')

    def test_brand_filter(self):
        self.client.login(email='user@user.com', password='password456')

        response = self.client.get(reverse('index'), {'brand': 'Apple'})
        self.assertContains(response, 'Reparación de pantalla IPhone 13')
        self.assertNotContains(response, 'Reparación de batería Samsung A20')