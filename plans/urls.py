from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import plans_view

app_name = 'plans'

urlpatterns = [
       path('list/', plans_view, name='list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)