from django.conf import settings

from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

# from django.contrib.auth.models import User
from accounts.models import User
from django.http import HttpResponse
from django.views import View

from payments.models import Payment
from .models import Coupon
from .forms import CouponApplyForm
from .validations import validate_coupon



@require_POST
def coupon_apply(request, payment_id=None):
    now = timezone.now()
    # payment = Payment.objects.get(id=payment_id)

    # if not payment.user == request.user:
    #     raise Http404

    form = CouponApplyForm(request.POST)
    if form.is_valid():
        coupon_code = form.cleaned_data['code']
        user = User.objects.get(username=request.user.username)
        
        status = validate_coupon(coupon_code=coupon_code, user=user)
        if status['valid']:
            coupon = Coupon.objects.get(code=coupon_code)
            coupon.use_coupon(user=user)
            request.session['coupon_id'] = coupon.id
            # print("=========status valid coupon=============", request.session['coupon_id'])
        else:
            request.session['coupon_id'] = None
            # print("=========status invalid coupon=============")

    return redirect('payments:payment_coupon', payment_id=payment_id)
    # return redirect('/payments/initiate/%s/' %(payment_id))






# class UseCouponView(View):
#     def get(self, request, *args, **kwargs):
#         coupon_code = request.GET.get("coupon_code")
#         user = User.objects.get(username=request.user.username)
#         payment_id = 121 #self.kwargs['payment_id']
        
#         status = validate_coupon(coupon_code=coupon_code, user=user)
#         if status['valid']:
#             coupon = Coupon.objects.get(code=coupon_code)
#             coupon.use_coupon(user=user)
#             request.session['coupon_id'] = coupon.id
#         else:
#             request.session['coupon_id'] = None
        
#             # return HttpResponse("OK")

#         # return HttpResponse(status['message'])
#         return redirect('payments:payment_coupon', payment_id=payment_id)


# return redirect('payments:payment_coupon', payment_id=payment_id)


# /use-coupon/?coupon_code=COUPONTEST01


