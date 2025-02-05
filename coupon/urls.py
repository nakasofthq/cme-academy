from django.urls import path
from . import views


app_name = 'coupon'

urlpatterns = [
    path("apply/<int:payment_id>/", views.coupon_apply, name="apply"),
    # path("apply/<int:payment_id>/", views.UseCouponView.as_view(), name="apply"),
    # path("detail/<slug:slug>/", CourseDetailView.as_view(), name="detail"),
   ]