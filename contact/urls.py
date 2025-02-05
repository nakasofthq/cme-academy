"""greenfieldhmo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from .views import contact, contact_sent#, quote_request, providers_registration, providers_registration_sent
# from authcode.views import home as pacg
# from capitation.views import home as cpar

app_name = 'contact'

urlpatterns = [
    path('', contact, name="contact"),
    path('sent/', contact_sent, name="contact-sent"),
    # path(r'quote-request/', quote_request, name="quote_request"),
    # path(r'providers/registration/', providers_registration, name="providers_registration"),
    # path(r'providers/registration/sent/', providers_registration_sent, name="providers_registration_sent"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

