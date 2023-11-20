
from django.contrib import admin
from django.urls import path, include
from core.views import index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',index,name='index'), 
    path('admin/', admin.site.urls),
    path('usuario/', include('custom_user.urls')),
    path('shoppingCart/', include('shoppingCart.urls')),
    path('product/', include('product.urls')),
    path('checkout/', include('order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
