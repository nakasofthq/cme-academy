"""
URL configuration for cme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views import defaults as default_views
from .views import home_view, about_view, privacy_view, terms_view, disclaimer_view, sales_page_view, channel_page_view #Home, AboutUs, Privacy, Terms, Disclaimer#, CourseList, CourseDetail



urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('privacy/', privacy_view, name='privacy'),
    path('terms/', terms_view, name='terms'),
    path('disclaimer/', disclaimer_view, name='disclaimer'),
    path('community/', sales_page_view, name='sales_page'),
    path('channel/', channel_page_view, name='channel_page'),

    # path("programs/", include("courses.urls")),
    # path('about/', AboutUs.as_view(), name='about'),
    # path('faq/', Faq.as_view(), name='faq'),
    # path('privacy/', Privacy.as_view(), name='privacy'),
    # path('terms/', Terms.as_view(), name='terms'),
    # path('disclaimer/', Disclaimer.as_view(), name='disclaimer'),
    # path('contact/',include('contact.urls', namespace = 'contact')),
    
    # path("programs/", include("courses.urls", namespace = 'courses')),
    # path('courses/', CourseList.as_view(), name='courses'),
    # path('courses/detail/', CourseDetail.as_view(), name='courses-detail'),
    # path('dashboard/', home, name="dashboard"),    
    # path('contact/', Contact.as_view(), name='contact'),
    # path('accounts/',include('accounts.urls', namespace = 'accounts')),
    # path('registration/',include('registration.urls', namespace = 'registration')),
    # path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    # path('ns-admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




