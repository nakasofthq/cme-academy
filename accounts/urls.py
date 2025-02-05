from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
# from .views import home
from .views import register_view, login_view, logout_view #DashboardView, ProfileView, CategoryListView
from django.views.generic import TemplateView

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    # path('category/', TemplateView.as_view(template_name="dashboard/category.html")),
]


# urlpatterns = [
# path('login',views.login, name='login'),
# path('logout',views.logout, name='logout'),
# ]
