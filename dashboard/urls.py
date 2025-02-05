from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *



app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('courses/', course_list_view, name='course_list'),
    path("courses/<slug:slug>/", course_detail_view, name="course_detail"),
    # path("courses/pdf/<slug:slug>/", pdf_view, name="course_pdf"),

    path('messages/', message_view, name='message_list'),
    path('plans/', plans_view, name='plans'),
    path('affiliate/', affiliate_view, name='affiliate'),
    path('settings/faqs/', faqs_view, name='faqs'),
    path('settings/contact/', HelpCenterView.as_view(), name='contact'),
    path('settings/contact/sent/', message_sent, name="message_sent"),
    # path('settings/contact/', ContactCreateView.as_view(), name="contact"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
