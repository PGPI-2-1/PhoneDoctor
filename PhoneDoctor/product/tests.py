from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Brand, Category

class ProductInfoViewTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Ejemplo Brand')
        self.category = Category.objects.create(name = 'Ejmplo Category')
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")


        self.product = Product.objects.create(name='Ejemplo', price=100.0, description='Descripción de ejemplo', brand=self.brand, category= self.category, image = image_file)

    def test_product_info_view(self):
        url = reverse('product_info', args=[self.product.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['product'], self.product)

        self.assertTemplateUsed(response, 'product/info.html')

        self.assertContains(response, 'Ejemplo')
        self.assertContains(response, '100.0')
        self.assertContains(response, 'Descripción de ejemplo')

    def test_product_info_view_404(self):
        url = reverse('product_info', args=[999])

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'product/404.html')
