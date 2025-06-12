from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('store/', include('store.urls')),

    path('carts/', include('carts.urls')),

    path('accounts/', include('accounts.urls')),

]
# For Media files in development, Only if I have MEDIA_URL and MEDIA_ROOT set in settings.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
