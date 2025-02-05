try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

import requests
from unicodedata import category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, FormView, CreateView, View, DetailView, TemplateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils import timezone

from courses.models import Course

# from .mixins import LoginRequiredMixin, StaffRequiredMixin
# from invoice.models import Client







def home_view(request):
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        data = requests.get(url).json()
    except:
        data = []

    # return HttpResponse(data)

    context = {
        'data': data,
        'course_list': Course.objects.all().order_by('-created'),
    }

    return render(request, 'index.html', context)



def about_view(request):
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        data = requests.get(url).json()
    except:
        data = []

    context = {'data': data}
    return render(request, 'about.html', context)


def privacy_view(request):
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        data = requests.get(url).json()
    except:
        data = []

    context = {'data': data}
    return render(request, 'privacy.html', context)


def terms_view(request):
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        data = requests.get(url).json()
    except:
        data = []

    context = {'data': data}
    return render(request, 'terms.html', context)


def disclaimer_view(request):
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        data = requests.get(url).json()
    except:
        data = []

    context = {'data': data}
    return render(request, 'disclaimer.html', context)



def sales_page_view(request):
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        data = requests.get(url).json()
    except:
        data = []

    context = {'data': data}
    return render(request, 'sales_page.html', context)



def channel_page_view(request):
    try:
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        data = requests.get(url).json()
    except:
        data = []

    context = {'data': data}
    return render(request, 'channel_page.html', context)




















# class Home(View):
#     # form_class = MyForm
#     # initial = {'key': 'value'}
#     template_name = 'index.html'

#     def get(self, request, *args, **kwargs):
#         # form = self.form_class(initial=self.initial)
#         # today = timezone.now().date()
#         context = {
#         'course_list': Course.objects.all(),
#             # 'today': today,
#             # 'blog_list': Post.objects.active()
#             }
#         return render(request, self.template_name, context)

#     # # def post(self, request, *args, **kwargs):
#     # #     form = self.form_class(request.POST)
#     # #     if form.is_valid():
#     # #         # <process form cleaned data>
#     # #         return HttpResponseRedirect('/success/')

#     # #     return render(request, self.template_name, {'form': form})

#     # def get_context_data(self, **kwargs):
#     #     # ==Call the base implementation first to get a context
#     #     context = super().get_context_data(**kwargs)
#     #     context['blog_list'] = Post.objects.active()
#     #     context['today'] = timezone.now().date()
#     #     return context




# class CourseList(View):
#     template_name = 'courses/course-list.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})


# class CourseDetail(View):
#     template_name = 'courses/course-detail.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})


# class AboutUs(View):
#     template_name = 'about.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})


# class Faq(View):
#     template_name = 'faq.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})



# class Privacy(View):
#     template_name = 'privacy.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})



# class Terms(View):
#     template_name = 'terms.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})




# class Disclaimer(View):
#     template_name = 'disclaimer.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {})



