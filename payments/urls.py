# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import path
from . import views
# from django.views.generic import TemplateView

app_name = 'payments'

urlpatterns = [
    path('initiate/', views.payment_initiate, name='payment_initiate'),
    path('initiate/<str:payment_id>/', views.payment_coupon, name='payment_coupon'),
    path('verify/<str:ref>/', views.payment_verify, name='payment_verify'),
]


