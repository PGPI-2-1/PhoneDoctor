from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from order.models import Order
from order.views import is_staff, order_admin_view
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser

class OrderViewsTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba con permisos de administrador
        self.admin_user = get_user_model().objects.create_user(
            email='admin@admin.com',
            password='password123',
            is_staff=True,
        )

        # Crear un usuario de prueba sin permisos de administrador
        self.normal_user = get_user_model().objects.create_user(
            email='user@user.com',
            password='password123',
            is_staff=False,
        )

        # Crear una orden de prueba
        self.order = Order.objects.create(
            address='Calle Test 123',
            email='test@example.com',
            status=Order.StatusChoices.PAGADO,
            precio_total=100.0,
        )

        # Configurar el objeto RequestFactory
        self.factory = RequestFactory()

    def test_is_staff_function(self):
        # Probar si la función is_staff devuelve True para un usuario con permisos de administrador
        self.assertTrue(is_staff(self.admin_user))

        # Probar si la función is_staff devuelve False para un usuario sin permisos de administrador
        self.assertFalse(is_staff(self.normal_user))

    def test_order_admin_view_authenticated_staff_user(self):
        # Probar si un usuario autenticado con permisos de administrador puede acceder a order_admin_view
        request = self.factory.get(reverse('order_admin_view'))
        request.user = self.admin_user
        response = order_admin_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Panel de Ventas')
        self.assertContains(response, str(self.order.id))


    def test_order_admin_view_unauthenticated_user(self):
        # Probar si un usuario no autenticado es redirigido a la página de inicio de sesión
        request = self.factory.get(reverse('order_admin_view'))
        # Simula el middleware de autenticación asignando el usuario a la solicitud
        request.user = AnonymousUser()
        response = order_admin_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn('/user/login/', response.url)
        self.assertEqual(response.status_code, 302)

    def test_order_admin_view_non_staff_user(self):
        # Probar si un usuario no autorizado (sin permisos de administrador) recibe una respuesta denegada
        request = self.factory.get(reverse('order_admin_view'))
        request.user = self.normal_user
        response = order_admin_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn('/user/login/', response.url)
        self.assertEqual(response.status_code, 302)
