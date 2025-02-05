import requests
from unicodedata import category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, FormView, CreateView, View, DetailView, TemplateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils import timezone

from affiliates.models import Affiliate, UserAffiliate, AffiliateSubscription




# class AffiliateView(View):
#     template_name = 'affiliates/list.html'

#     def get(self, request, *args, **kwargs):
#         current_affiliate = UserAffiliate.objects.filter(affiliate__title="free").first()
#         if self.request.user.is_authenticated:
#             user_affiliate = UserAffiliate.objects.filter(user=self.request.user).first()
#             if user_affiliate is not None:
#                 current_affiliate = user_affiliate.affiliate
#         context = {
#             'category': 'affiliate',
#             'current_affiliate': str(current_affiliate),
#             'object': Affiliate.objects.exclude(title="free").first()
#         }
#         return render(request, self.template_name, context)




def affiliate_view(request):
  plan_list = Affiliate.objects.exclude(title="free")
  current_plan = []
  try:
    if request.user.is_authenticated:
      user_plan = UserAffiliate.objects.filter(user=request.user).first()
      user_subscription = AffiliateSubscription.objects.filter(user_affiliate=user_plan).first()
      # if user_plan is not None and not user_subscription.is_expired() and user_subscription.is_active():
      if user_plan is not None and user_subscription is not None and not user_subscription.is_expired() and user_subscription.is_active():
        current_plan = user_plan.affiliate # UserAffiliate.objects.filter(affiliate__title="free").first()
      # print("=====", user_subscription.is_expired(), "ACTIVE", user_subscription.is_active())
  except:
    pass
  
  try:
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url).json()
  except:
    data = []

  context = {
      'data': data,
      'category': 'affiliate',
      'current_plan': current_plan,
      'object_list': plan_list,
      'object': Affiliate.objects.exclude(title="free").first()
    }

  return render(request, 'affiliates/list.html', context)

