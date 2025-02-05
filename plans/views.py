import requests
from django.shortcuts import render

from django.views.generic import ListView
from plans.models import Plan, UserPlan, Subscription





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
  
  # try:
  #   url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
  #   data = requests.get(url).json()
  # except:
  #   data = []

  context = {
    # "data": data,
    "category": "plan",
    "object_list": plan_list,
    "current_plan": current_plan,
    }

  return render(request, 'plans/list.html', context)







# class PlanView(ListView):
#     model = Plan
#     template_name = 'plans/list.html'

#     def get_user_plan(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             user_plan = UserPlan.objects.filter(user=self.request.user).first()
#             if user_plan:
#                 return user_plan
#         return None

#     def get_queryset(self, *args, **kwargs):
#         qs = super().get_queryset(**kwargs)
#         qs = qs.exclude(title="free")
#         return qs

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         current_plan = UserPlan.objects.filter(plan__title="free").first()
#         user_plan = self.get_user_plan(self.request)
#         if user_plan is not None:
#             current_plan = user_plan.plan 
#         context['current_plan'] = str(current_plan)
#         context['category'] = 'plan'
#         return context





