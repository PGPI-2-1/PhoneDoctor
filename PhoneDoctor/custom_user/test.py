from django.test import TestCase
from django.urls import reverse
class User_admin_ViewTest(TestCase):

    def test_product_info_view_404(self):
        url = reverse('user_admin_view')

        response = self.client.get(url)
        self.assertTemplateUsed(response, '403.html')
