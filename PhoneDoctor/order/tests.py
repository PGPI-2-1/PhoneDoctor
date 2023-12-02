from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from order.forms import NewReviewForm
from custom_user.models import User
from order.models import Order, Review
from shoppingCart.models import CartItem
from product.models import Product, Brand, Category

# Create your tests here.

# TEST REVIEW

class ReviewViewTest(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name='Ejemplo Brand')
        self.category = Category.objects.create(name = 'Ejmplo Category')
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.product = Product.objects.create(name='Ejemplo', price=100.0, description='Descripción de ejemplo', brand=self.brand, category= self.category, image = image_file)

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
        self.order = Order.objects.create(user = self.normal_user, address = "ETSII", email = self.normal_user.email, status = Order.StatusChoices.PAGADO, precio_total = 100.)
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
        print(form.errors)


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
        self.brand = Brand.objects.create(name='Ejemplo Brand')
        self.category = Category.objects.create(name = 'Ejmplo Category')
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.product = Product.objects.create(name='Ejemplo', price=100.0, description='Descripción de ejemplo', brand=self.brand, category= self.category, image = image_file)

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
        self.order = Order.objects.create(user = self.normal_user, address = "ETSII", email = self.normal_user.email, status = Order.StatusChoices.PAGADO, precio_total = 100.)
        self.order_no_review = Order.objects.create(user = self.normal_user, address = "ETSII", email = self.normal_user.email, status = Order.StatusChoices.PAGADO, precio_total = 100.)

        self.order.items.add(self.cartItem)

        self.review = Review.objects.create(title = "Titulo de review", description = "Descripcion de review")
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
           

   


        



