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
# from .views import Home, CourseList, CourseDetail, AboutUs, Faq, Privacy, Terms, Disclaimer





# customizing admin interface 
admin.site.site_header = 'CME Academy'
admin.site.site_title = 'CME Academy'
admin.site.index_title = 'CME Administration'



urlpatterns = [
    # path('', Home.as_view(), name='home'),
    # path("programs/", include("courses.urls")),
    # path('about/', AboutUs.as_view(), name='about'),
    # path('faq/', Faq.as_view(), name='faq'),
    # path('privacy/', Privacy.as_view(), name='privacy'),
    # path('terms/', Terms.as_view(), name='terms'),
    # path('disclaimer/', Disclaimer.as_view(), name='disclaimer'),
    # path('courses/', CourseList.as_view(), name='courses'),
    # path('courses/detail/', CourseDetail.as_view(), name='courses-detail'), 
    # path('contact/', Contact.as_view(), name='contact'),
    # path('registration/',include('registration.urls', namespace = 'registration')),
    path('contact/',include('contact.urls', namespace = 'contact')),    
    path("courses/", include("courses.urls", namespace = 'courses')),
    path("plans/", include("plans.urls", namespace = 'plans')),
    path("affiliates/", include("affiliates.urls", namespace = 'affiliates')),
    path('payments/',include('payments.urls', namespace = 'payments')), 
    path('dashboard/',include('dashboard.urls', namespace = 'dashboard')),
    path('coupon/',include('coupon.urls', namespace = 'coupon')),
    # path('coupons/',include('coupons.urls', namespace = 'coupons')),
    path('accounts/',include('accounts.urls', namespace = 'accounts')),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'), #auth library
    # urls handling WYSIWYG editor
    path('summernote/', include('django_summernote.urls')), 
    path('ns-admin/', admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]


