# myapp/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from custom_user.models import User
from product.models import Brand, Category, Product
from order.models import Order, Review
from shoppingCart.models import CartItem
from order.forms import NewReviewForm

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

        self.cartItem = CartItem.objects.create(user = self.normal_user, product = self.iphone_product, quantity = 1,  is_processed = True)
        self.order = Order.objects.create(user = self.normal_user, address = "ETSII", email = self.normal_user.email, status = Order.StatusChoices.PROCESADO, precio_total = 100., id_tracking = "ss1033fs")
        self.order.items.add(self.cartItem)

        self.client = Client()

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

    def test_review_status_change_view(self):

        self.client.login(email='user@user.com', password='password123')
        url = reverse('order_review', args=[self.order.pk])

        
        data = {
            'id': 1,
            'title': 'Mi Título de Revisión',
            'description': 'Mi Descripción de Revisión',
        }
        form = NewReviewForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
    
        review = Review.objects.get(pk=1)
        self.assertEqual(review.title, data['title'])
        self.assertEqual(review.description, data['description'])
        self.assertEqual(review.is_accepted, 'pendiente')

        self.client.logout()
        self.client.login(email='admin@admin.com', password='password123')

        url = reverse('order_review_admin', args=[self.order.pk])
        
        self.assertEqual(review.title, data['title'])
        self.assertEqual(review.description, data['description'])
        self.assertEqual(review.is_accepted, 'pendiente')

        # Cambiar el estado is_accepted a 'aceptado'
        url_change_status = reverse('order_review_admin', args=[self.order.pk])
        data_change_status = {
            'is_accepted': 'aceptado',
        }
        response_change_status = self.client.post(url_change_status, data_change_status)

        self.assertEqual(response_change_status.status_code, 200)

        review.refresh_from_db()

        self.assertEqual(review.is_accepted, 'aceptado')

        self.client.logout()

        self.client.login(email='user@user.com', password='password123')
        url = reverse('order_review', args=[self.order.pk])

        self.assertEqual(review.is_accepted, 'aceptado')
