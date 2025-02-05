
import requests
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required, user_passes_test

from cme.mixins import (
    # LoginRequiredMixin, 
    # StaffRequiredMixin, 
    # ICTStaffRequiredMixin,
    # MedicalStaffRequiredMixin, 
    # AjaxRequiredMixin,
    SubmitBtnMixin,
    # FilterMixin
    ) 

from plans.models import Plan, UserPlan, Subscription
from affiliates.models import Affiliate, UserAffiliate, AffiliateSubscription
from courses.models import Course
from .models import HelpCenter
from .forms import ProfileForm, HelpCenterForm



@login_required
def dashboard_view(request):
  try:
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url).json()
  except:
    data = []
  
  # return HttpResponse(data)

  context = {'data': data}

  return render(request, 'dashboard/index.html', context)



@login_required
def profile_view(request):
  
  if request.method == 'POST':
    form = ProfileForm(data=request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        # return redirect('dashboard:message_sent')
        messages.success(request, "Profile updated successfully!")
  else:
    form = ProfileForm(instance=request.user)

  context = {
    'user': request.user,
    'form': form,
    'submit_btn': 'Update Profile',
    } 

  return render(request, 'dashboard/settings-profile.html', context)






@login_required
def message_view(request):
  context = {
    'user': request.user
    }

  return render(request, 'dashboard/message-list.html', context)



@login_required
def faqs_view(request):
  context = {
    'user': request.user
    }

  return render(request, 'dashboard/settings-faqs.html', context)


@login_required
def contact_view(request):
  context = {
    'user': request.user
    }

  return render(request, 'dashboard/settings-contact.html', context)


# @login_required
# def profile_view(request):
#   context = {
#     'user': request.user
#     }

#   return render(request, 'dashboard/settings-profile.html', context)






# def pdf_view(request):
#     try:
#         return FileResponse(open('foobar.pdf', 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise Http404()



# def pdf_view(request):
#   try:
#       return FileResponse(open('foobar.pdf', 'rb'), content_type='application/pdf')
#   except FileNotFoundError:
#       raise Http404()





@login_required
def course_list_view(request):
  grade_0 = grade_1 = grade_2 = grade_3 = []
  try:
    if request.user.is_authenticated:
      user_plan = UserPlan.objects.filter(user=request.user).first()
      user_subscription = Subscription.objects.filter(user_plan=user_plan).first()

      if user_plan and user_subscription and user_subscription.is_active() and not user_subscription.is_expired():

        if user_plan.plan.title == "free":
          grade_0 = Course.objects.all().filter(plan__title='free')
        elif user_plan.plan.title == "basic":
          grade_0 = Course.objects.all().filter(plan__title='free')
          grade_1 = Course.objects.all().filter(plan__title='basic')
        elif user_plan.plan.title == "advance":
          grade_0 = Course.objects.all().filter(plan__title='free')
          grade_1 = Course.objects.all().filter(plan__title='basic')
          grade_2 = Course.objects.all().filter(plan__title='advance')
        elif user_plan.plan.title == "pro":
          grade_0 = Course.objects.all().filter(plan__title='free')
          grade_1 = Course.objects.all().filter(plan__title='basic')
          grade_2 = Course.objects.all().filter(plan__title='advance')
          grade_3 = Course.objects.all().filter(plan__title='pro')
        else:
          pass
          # grade_0 = grade_1 = grade_2 = grade_3 = []

    # query = request.GET.get("search")
    # if query:
    #   qs = qs.filter(
    #           Q(title__iexact=query)|
    #           Q(description__icontains=query)
    #           ).distinct()
  except:
    pass


  context = {
    # "object_list": qs,
    "course_list": Course.objects.all(),
    "grade_0": grade_0,
    "grade_1": grade_1,
    "grade_2": grade_2,
    "grade_3": grade_3,
    }
  return render(request, 'dashboard/course-list.html', context)





@login_required
def course_detail_view(request, slug):
  obj = get_object_or_404(Course, slug=slug)

  if request.user.is_authenticated:
    user_plan = UserPlan.objects.filter(user=request.user).first()
    user_subscription = Subscription.objects.filter(user_plan=user_plan).first()
    if user_plan and not user_subscription.is_expired() and user_subscription.is_active():

      if user_plan.get_user_grade() < obj.get_course_grade():
        # raise Http404()
        context = {
          "content": "You are not registered for this course!"
          }
        return render(request, 'dashboard/static-page.html', context)
    else:        
      # raise Http403()
      context = {
          "content": "You are not registered for this course!"
        }
      return render(request, 'dashboard/static-page.html', context)

  
  context = {
    "object": obj,
    "course_list": Course.objects.all(),
    }
  return render(request, 'dashboard/course-detail.html', context)






# from django.shortcuts import render
# from django.http import FileResponse, Http404





# import os
# from django.http import FileResponse, Http404


# def pdf_view(request, slug):
#   obj = get_object_or_404(Course, slug=slug)
#   print("===PDF URL===", obj.upload_file.url)
#   pdf_path = '127.0.0.1:8003%s' %(obj.upload_file.url)
#   file_path = r'127.0.0.1:8003%s' %(obj.upload_file.url)
#   print("===PDF EXIST===", os.path.isfile(file_path), file_path)
#   print("===PDF PATH===", '%s' %(pdf_path))
#   try:
#     return FileResponse(open(f'{pdf_path}', 'rb'), content_type='application/pdf')
#   except FileNotFoundError:
#     raise Http404()


# file_path = r'C:\Users\myname\Rprojects\Reports_scraping\data_scraped\icnarc_29052020\icnarc_200529.pdf'
# print( os.path.isfile(file_path))



# def pdf_view(request, slug):
#   obj = get_object_or_404(Course, slug=slug)
#   print("===PDF URL===", obj.upload_file.url)
#   pdf_path = '127.0.0.1:8003%s' %(obj.upload_file.url)
#   file_path = r'127.0.0.1:8003%s' %(obj.upload_file.url)
#   print("===PDF EXIST===", os.path.isfile(file_path), file_path)
#   print("===PDF PATH===", f'{pdf_path}')
#   with open('%s' %(pdf_path), 'rb') as pdf:
#     response = HttpResponse(pdf.read(),content_type='application/pdf')
#     response['Content-Disposition'] = 'filename=upload_file.pdf'
#     return response


# content = f"inline; filename={filename}"


# def pdf_view(request, slug):
#   obj = get_object_or_404(Course, slug=slug)
#   print("===PDF File===", 'obj.upload_file')
#   pdf_path = "obj.upload_file.url"
#   with open(pdf_path, 'rb') as pdf:
#     response = HttpResponse(pdf.read(), mimetype='application/pdf')
#     response['Content-Disposition'] = 'inline; filename=upload_file_name.pdf'
#     return response
#   pdf.closed






# def pdf_view(request, slug):
#   obj = get_object_or_404(Course, slug=slug)
#   # try:
#   #     return FileResponse(open('<file name with path>', 'rb'), content_type='application/pdf')
#   # except FileNotFoundError:
#   #     raise Http404('not found')

#   try:
#       return FileResponse(open(obj.upload_file, 'rb'), content_type='application/pdf')
#   except FileNotFoundError:
#       raise Http404()


# def pdf_view(request, slug):
#   obj = get_object_or_404(Course, slug=slug)
#   with open(obj.upload_file, 'rb') as pdf:
#     response = HttpResponse(pdf.read(),content_type='application/pdf')
#     response['Content-Disposition'] = 'filename=some_file.pdf'
#     return response








@login_required
def plans_view(request):
  plan_list = Plan.objects.exclude(title="free")
  current_plan = []
  try:
    if request.user.is_authenticated:
      user_plan = UserPlan.objects.filter(user=request.user).first()
      user_subscription = Subscription.objects.filter(user_plan=user_plan).first()
      # if user_plan is not None and not user_subscription.is_expired() and user_subscription.is_active():
      if user_plan is not None and user_subscription is not None and not user_subscription.is_expired() and user_subscription.is_active():
        current_plan = user_plan.plan #UserPlan.objects.filter(plan__title="free").first()
  except:
    pass

  context = {
    "category": "plan",
    "current_plan": current_plan,
    "object_list": plan_list,
    }

  return render(request, 'dashboard/plan-list.html', context)




@login_required
def affiliate_view(request):
  plan_list = Affiliate.objects.exclude(title="free")

  current_plan = []
  try:
    if request.user.is_authenticated:
      user_plan = UserAffiliate.objects.filter(user=request.user).first()
      user_subscription = AffiliateSubscription.objects.filter(user_affiliate=user_plan).first()
      if user_plan and user_subscription and not user_subscription.is_expired() and user_subscription.is_active():
        current_plan = user_plan # UserAffiliate.objects.filter(affiliate__title="free").first()
      # print("=====", user_subscription.is_expired(), "ACTIVE", user_subscription.is_active())
  except:
    pass

  context = {
      'category': 'affiliate',
      'current_plan': current_plan,
      'object_list': plan_list
    }

  return render(request, 'dashboard/affiliate-list.html', context)













# class ContactCreateView(LoginRequiredMixin, SubmitBtnMixin, CreateView):
#     template_name = "dashboard/settings-contact.html"
#     model = Contact
#     form_class = ContactForm 
#     success_url = reverse_lazy('contact:message_sent')
#     # submit_btn = "Add Contact"

#     def form_valid(self, form):
#         form_last_name = form.cleaned_data.get("last_name")
#         form_first_name = form.cleaned_data.get("first_name")
#         form_phone = form.cleaned_data.get("phone")
#         form_email = form.cleaned_data.get("email")
#         form_company = form.cleaned_data.get("company")
#         form_subject = form.cleaned_data.get("subject")
#         form_message = form.cleaned_data.get("message")

#         subject = 'From Insure Support Form: %s' %(form_subject)
#         from_email = settings.DEFAULT_FROM_EMAIL
#         to_email = ['dsixnine@gmail.com'] #['support@greenfieldhmo.com']
#         contact_message = "\n Last Name: %s \n First Name: %s \n Phone: %s \n Email: %s \n Company: %s \n Subject: %s \n\n Message: \n %s" %(
#             form_last_name,
#             form_first_name,
#             form_phone,
#             form_email,
#             form_company,
#             form_subject,
#             form_message)

#         send_mail(
#             subject,
#             contact_message,
#             from_email,
#             [to_email],
#             fail_silently=False,
#         )

#         valid_data = super().form_valid(form)
#         messages.success(self.request, "Message Sent")
#         return valid_data

#     def form_invalid(self, form):
#         messages.success(self.request, "Message Failed")
#         return super().form_invalid(form)

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         # context["provider_list"] = Provider.objects.all() 
#         # context["client_list"] = Client.objects.all() 
#         return context






class HelpCenterView(SubmitBtnMixin, CreateView):
    template_name = "dashboard/settings-contact.html"
    model = HelpCenter
    form_class = HelpCenterForm 
    success_url = reverse_lazy('dashboard:message_sent')
    submit_btn = "Submit Message"

    def form_valid(self, form):
        form.instance.user = self.request.user

        valid_data = super().form_valid(form)
        messages.success(self.request, "Message Sent")
        return valid_data

    def form_invalid(self, form):
        messages.danger(self.request, "Message Failed")
        return super().form_invalid(form)



def message_sent(request):
    form = HelpCenterForm(request.POST or None)
    # contact_title = 'Your message has been sent. Thank you!'
    context = {
        "form": form,
    }
    return render(request, "dashboard/settings-contact-sent.html", context)





