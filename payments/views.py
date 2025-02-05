import datetime
import requests
from decimal import Decimal, FloatOperation
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse

from affiliates.models import Affiliate, UserAffiliate, AffiliateSubscription
from plans.models import Plan, UserPlan, Subscription
from .models import Payment, UserWallet
from coupon.models import Coupon, Discount
from coupon.forms import CouponApplyForm




@login_required(login_url="accounts:login")
def payment_initiate(request):

    if request.method == "POST":
        category = request.POST['category']
        plan_type = request.POST['plan_type']
        duration = request.POST['plan_duration']
        price = request.POST['plan_price']
        email = request.user.email
        user = request.user

        amount = Decimal(price)*Decimal(duration)

        payment = Payment.objects.create(amount=amount, category=category, plan_type=plan_type, duration=duration, email=email, user=user)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
            'amount_value': payment.amount_value(),
            'coupon_apply_form': CouponApplyForm(),
        }
        return render(request, 'payments/payment_confirmation.html', context)

    return redirect("plans:list")





@login_required(login_url="accounts:login")
def payment_coupon(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user__username=request.user.username)

    coupon_id = request.session['coupon_id']
    
    try:
        coupon = Coupon.objects.get(id=coupon_id)
        discount = Discount()
        discount.value = coupon.discount.value
        discount.is_percentage = coupon.discount.is_percentage
        discount.save()
        # print("=====DISCOUNT========", discount.value, coupon.discount.value, discount.is_percentage, coupon.discount.is_percentage)
        payment.coupon = coupon
        # payment.discount = discount
        payment.save()
        # print("=========valid coupon payment=============", coupon_id)
        # messages.success(self.request, "Coupon Successful")
        coupon_message = "Coupon Successful"
    except Coupon.DoesNotExist:        
        # print("=========invalid coupon payment=============", coupon_id)
        # messages.danger(self.request, "Coupon Invalid")
        coupon_message = "Coupon Invalid"
        pass

    context = {
        'payment': payment,
        'field_values': request.POST,
        'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
        'amount_value': payment.amount_value(),
        'coupon_apply_form': CouponApplyForm(),
        'coupon_message': coupon_message,
    }
    return render(request, 'payments/payment_confirmation.html', context)





@login_required(login_url="accounts:login")
def payment_verify(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        category = payment.category
        # print("===Category===", category)
        if category == 'plan':
            #=== update userPlan and subscription ===#
            user_plan = UserPlan.objects.get(user=request.user)
            user_plan.plan = Plan.objects.filter(title=payment.plan_type).first()
            # user_plan.plan = payment.plan
            user_plan.save()

            subscription = Subscription.objects.get(user_plan=user_plan)
            # print("===Subscription===", subscription)
            subscription.subscription_period = payment.duration
            subscription.start_date = datetime.date.today()
            subscription.end_date = datetime.date.today() + relativedelta(months=int(payment.duration))
            subscription.amount = payment.amount 
            subscription.fee_status = 'paid'
            subscription.save()
            # print("===Sub details===", subscription.subscription_period, subscription.start_date, subscription.end_date, subscription.amount, subscription.fee_status)

        elif category == 'affiliate':
            #=== update userPlan and subscription ===#
            user_affiliate, created = UserAffiliate.objects.get_or_create(
                user=request.user,
                defaults={'affiliate': Affiliate.objects.filter(title=payment.plan_type).first()},
            )
            user_affiliate.create_code()
            user_affiliate.save() 
            # print("===User Affiliate===", user_affiliate)

            subscription, created = AffiliateSubscription.objects.get_or_create(
                user_affiliate=user_affiliate,
                defaults={
                    'subscription_period': payment.duration,
                    'start_date': datetime.date.today(),
                    'end_date': datetime.date.today() + relativedelta(months=int(payment.duration)),
                    'amount': payment.amount,
                    'fee_status': 'paid',
                },
            )
            # print("===Subscription===", subscription)

        else:
            raise Http404

        # #=== update user-wallet ===#
        # user_wallet = UserWallet.objects.get(user=request.user)
        # user_wallet.balance += payment.amount
        # user_wallet.save()
        
        # print(request.user.username, " funded wallet successfully")
  
        # # To display cryptocurrency current prices on top of the navbar
        # try:
        #     url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
        #     data = requests.get(url).json()
        # except:
        #     data = []

        # context = {
        #     'data': data,
        # }

        # return render(request, "payments/payment_successful.html", {})
    return render(request, "payments/payment_successful.html", {})


