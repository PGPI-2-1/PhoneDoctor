from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from order.views import generate_unique_random_string
from order.forms import NewReviewForm
from custom_user.models import User
from order.models import Order, Review
from shoppingCart.models import CartItem
from product.models import Product, Brand, Category
from django.contrib.auth import get_user_model
from order.views import is_staff, order_admin_view
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser


# Create your tests here.

# TEST REVIEW

class ReviewViewTest(TestCase):

    def setUp(self):
        tracking = generate_unique_random_string()
        self.brand = Brand.objects.create(name='Ejemplo Brand')
        self.category = Category.objects.create(name='Ejmplo Category')
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.product = Product.objects.create(name='Ejemplo', price=100.0, description='Descripción de ejemplo', brand=self.brand, category=self.category, image=image_file)

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
        self.cartItem = CartItem.objects.create(user = self.normal_user, product = self.product, quantity = 1,  is_processed = True)
        self.order = Order.objects.create(user = self.normal_user, address = "ETSII", email = self.normal_user.email, status = Order.StatusChoices.PROCESADO, precio_total = 100., id_tracking = tracking)
        self.order.items.add(self.cartItem)

        self.client = Client()

    def test_review_form_view(self):

        self.client.login(email='user@user.com', password='password123')

        url = reverse('order_review', args=[self.order.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"', count=1)

    def test_review_form_negative_view(self):

        url = reverse('order_review', args=[self.order.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'form.html')

    def test_create_review_view(self):

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

    def test_create_review_negative_view(self):

        self.client.login(email='user@user.com', password='password123')
        url = reverse('order_review', args=[self.order.pk])

        data = {
            'id': 1,
            'title': 'Mi Título de Revisión',
        }

        form = NewReviewForm(data={})

        self.assertFalse(form.is_valid())
        self.assertTrue('description' in form.errors)

        data = {
            'id': 1,
            'description': 'Mi description de Revisión',
        }

        form = NewReviewForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue('title' in form.errors)

        form = NewReviewForm(data={})

        self.assertFalse(form.is_valid())
        self.assertTrue('title' in form.errors)
        self.assertTrue('description' in form.errors)

    def test_review_create_title_not_valid(self):
        self.client.login(email='user@user.com', password='password123')
        url = reverse('order_review', args=[self.order.pk])

        data = {
            'title': 'Esto es un titulo con mas de 50 caracteres para el t',
            'description': 'Mi Descripción de Revisión',
        }
        form = NewReviewForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('title' in form.errors)

    def test_review_create_description_not_valid(self):
        self.client.login(email='user@user.com', password='password123')
        url = reverse('order_review', args=[self.order.pk])

        data = {
            'title': 'Titulo para la review',
            'description': 'La reparación de la pantalla de mi móvil fue una experiencia increíble. El equipo de técnicos mostró profesionalismo y destreza. La rapidez con la que resolvieron el problema fue impresionante. Mi pantalla ahora luce impecable, devolviéndole la vida a mi d',
        }
        form = NewReviewForm(data)
        self.assertFalse(form.is_valid())
        self.assertTrue('description' in form.errors)


class ReviewAdminViewTest(TestCase):

    def setUp(self):
        tracking1 = generate_unique_random_string()
        tracking2 = generate_unique_random_string()
        self.brand = Brand.objects.create(name='Ejemplo Brand')
        self.category = Category.objects.create(name='Ejmplo Category')
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.product = Product.objects.create(name='Ejemplo', price=100.0, description='Descripción de ejemplo', brand=self.brand, category=self.category, image=image_file)

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
        self.cartItem = CartItem.objects.create(user = self.normal_user, product = self.product, quantity = 1,  is_processed = True)
        self.order = Order.objects.create(user = self.normal_user, address = "ETSII", email = self.normal_user.email, status = Order.StatusChoices.PROCESADO, precio_total = 100., id_tracking = tracking1)
        self.order_no_review = Order.objects.create(user = self.normal_user, address = "ETSII", email = self.normal_user.email, status = Order.StatusChoices.PROCESADO, precio_total = 100., id_tracking = tracking2)

        self.order.items.add(self.cartItem)

        self.review = Review.objects.create(title="Titulo de review", description="Descripcion de review")
        self.order.review = self.review
        self.order.save()

        self.client = Client()

    def test_review_exists_view(self):

        self.client.login(email='admin@admin.com', password='password123')

        url = reverse('order_review_admin', args=[self.order.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Titulo de review', count=1)
        self.assertContains(response, 'Descripcion de review', count=1)

    def test_review_no_exists_view(self):

        self.client.login(email='admin@admin.com', password='password123')

        url = reverse('order_review_admin', args=[self.order_no_review.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
           
class OrderModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='testpassword')

    def test_order_creation(self):
        tracking = generate_unique_random_string()
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=self.user, product=product, quantity=2, is_processed=False)
        
        order = Order.objects.create(user=self.user, address='Test Address', email='test@example.com', status=Order.StatusChoices.PROCESADO, precio_total=20.0, id_tracking = tracking)
        order.items.add(cart_item)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.address, 'Test Address')
        self.assertEqual(order.email, 'test@example.com')
        self.assertEqual(order.status, Order.StatusChoices.PROCESADO)
        self.assertEqual(order.precio_total, 20.0)
        self.assertEqual(order.items.count(), 1)

    def test_generate_unique_random_string(self):
        result = generate_unique_random_string()
        self.assertIsNotNone(result)

        order = Order.objects.create(user=self.user, address='Test Address', email='test@example.com', status=Order.StatusChoices.PROCESADO, precio_total=20.0, id_tracking = result)
        order.save()

        self.assertIsNotNone(Order.objects.filter(id_tracking=result))

    def test_search_order(self):
        result = generate_unique_random_string()
        order = Order.objects.create(user=self.user, address='Test Address', email='test@example.com', status=Order.StatusChoices.PROCESADO, precio_total=20.0, id_tracking=result)
        order.save()

        url = reverse('search_order') + f'?q={result}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_bad_search_order(self):
        badresult = '37498274982379487'
        result = generate_unique_random_string()
        order = Order.objects.create(user=self.user, address='Test Address', email='test@example.com', status=Order.StatusChoices.PROCESADO, precio_total=20.0, id_tracking=result)
        order.save()

        url = reverse('search_order') + f'?q={badresult}'
        response = self.client.get(url)

        self.assertTemplateUsed(response, '404.html')


class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.brand = Brand.objects.create(name='Test Brand')

    def test_checkout_authenticated_user_cash(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=self.user, product=product, quantity=2, is_processed=False)
       
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.post(reverse('checkout'), {'address': 'Test Address', 'payment_option': 'contra_reembolso', 'delivery_option': Order.DeliveryOptions.CORREOS})
       
        self.assertEqual(response.status_code, 302) 
        order = Order.objects.get(user=self.user)
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(all(cart_item.is_processed for cart_item in CartItem.objects.filter(user=self.user)))

    def test_checkout_unauthenticated_user_cash(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=None, product=product, quantity=2, is_processed=False)

        response = self.client.post(reverse('checkout'), {'address': 'Test Address', 'email': 'test@example.com', 'delivery_option': Order.DeliveryOptions.DOMICILIO, 'payment_option': 'contra_reembolso'})
       
        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(user=None)
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(all(cart_item.is_processed for cart_item in CartItem.objects.filter(user=None)))

    def test_checkout_authenticated_user_credit_card(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=self.user, product=product, quantity=2, is_processed=False)
       
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.post(reverse('checkout'), {'address': 'Test Address', 'payment_option': 'tarjeta_credito', 'delivery_option': Order.DeliveryOptions.CORREOS, 'stripeToken': 'tok_visa'})
       
        self.assertEqual(response.status_code, 302) 
        order = Order.objects.get(user=self.user)
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(all(cart_item.is_processed for cart_item in CartItem.objects.filter(user=self.user)))

    def test_checkout_unauthenticated_user_credit_card(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=None, product=product, quantity=2, is_processed=False)

        response = self.client.post(reverse('checkout'), {'address': 'Test Address', 'email': 'test@example.com', 'delivery_option': Order.DeliveryOptions.DOMICILIO, 'payment_option': 'contra_reembolso', 'stripeToken': 'tok_visa'})
       
        self.assertEqual(response.status_code, 302)

        order = Order.objects.get(user=None)
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertTrue(all(cart_item.is_processed for cart_item in CartItem.objects.filter(user=None)))

    def test_checkout_empty_values(self):
        product = Product.objects.create(name='Test Product', price=10.0, brand=self.brand, category=self.category, quantity=5)
        cart_item = CartItem.objects.create(user=None, product=product, quantity=2, is_processed=False)

        response = self.client.post(reverse('checkout'))
       
        self.assertEqual(response.status_code, 200)

        order = Order.objects.filter(user=None).first()
        self.assertIsNone(order)

    
