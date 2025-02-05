
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.conf import settings
from decimal import Decimal

from .decorators import ajax_required




def superuser_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in and is a superuser member, 
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator






def staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def ict_staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='ICT').exists() and u.is_active and u.is_staff, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator












def medical_staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member and group member, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        # lambda u: u.is_active and u.is_staff and u.groups.filter(name='Medical').exists(),
        lambda u: u.is_superuser or u.groups.filter(name='Medical').exists() and u.is_active and u.is_staff, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator




def account_staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='Account').exists() and u.is_active and u.is_staff, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator



def adminhr_staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='AdminHR').exists() and u.is_active and u.is_staff, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator




def ict_staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='ICT').exists() and u.is_active and u.is_staff, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator









def insurer_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in and is in a category of users, 
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        # lambda u: u.is_active and u.is_staff and u.groups.filter(name='Medical').exists(),
        lambda u: u.is_active and u.is_insurer or u.is_superuser, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator



def provider_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_provider or u.is_superuser, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator



def enrollee_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=settings.LOGIN_URL):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_enrollee or u.is_superuser, 
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator









class AjaxRequiredMixin(object):
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class SuperuserRequiredMixin(object):
    @method_decorator(superuser_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)








class ICTStaffRequiredMixin(object):
    @method_decorator(ict_staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class MedicalStaffRequiredMixin(object):
    @method_decorator(medical_staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AccountStaffRequiredMixin(object):
    @method_decorator(account_staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AdminHRStaffRequiredMixin(object):
    @method_decorator(adminhr_staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)










class InsurerRequiredMixin(object):
    @method_decorator(insurer_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class ProviderRequiredMixin(object):
    @method_decorator(provider_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class EnrolleeRequiredMixin(object):
    @method_decorator(enrollee_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
# class EnrolleeRequiredMixin(object):
# 	@method_decorator(login_required)
# 	def dispatch(self, request, *args, **kwargs):
# 		if not self.request.user.is_enrollee:
# 			messages.success(self.request, "Enrollee Login Failed")
# 			return redirect('login')
# 		# if not self.request.user.profile.profile_image:
# 		# 	messages.success(self.request, "Upload your photo.")
# 		# 	return redirect('dashboard:profile_photo_update')
# 		return super().dispatch(request, *args, **kwargs)








class SubmitBtnMixin(object):
    submit_btn = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["submit_btn"] = self.submit_btn
        return context



# class MultiSlugMixin(object):
#     model = None

#     def get_object(self, *args, **kwargs):
#         slug = self.kwargs.get("slug")
#         ModelClass = self.model
#         if slug is not None:
#             try:
#                 obj = get_object_or_404(ModelClass, slug=slug)
#             except ModelClass.MultipleObjectsReturned:
#                 obj = ModelClass.objects.filter(slug=slug).order_by("-title").first()
#         else:
#             obj = super().get_object(*args, **kwargs)
#         return obj




# class FilterMixin(object):
#     filter_class = None
#     search_ordering_param = "ordering"

#     def get_queryset(self, *args, **kwargs):
#         try:
#             qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
#             return qs
#         except:
#             raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         qs = self.get_queryset()
#         ordering = self.request.GET.get(self.search_ordering_param)
#         if ordering:
#             qs = qs.order_by(ordering)
#         filter_class = self.filter_class
#         if filter_class:
#             f = filter_class(self.request.GET, queryset=qs)
#             f = f.qs
            
#             # show 12 buildings per page
#             paginator = Paginator(f, 12)
#             page = self.request.GET.get('page')
#             f = paginator.get_page(page)

#             context["object_list"] = f
#         return context









