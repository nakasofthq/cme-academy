from django.db import models
from decimal import Decimal
from django.conf import settings
# from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

import secrets
from cme.decorators import CATEGORY_CHOICES, DURATION_CHOICES, FEE_STATUS
from plans.models import Plan, UserPlan
from coupon.models import Coupon 
from .paystack  import  Paystack



# # Create your models here.
# class Payments(models.Model):
#     user = models.ForeignKey(UserPlan, on_delete=models.CASCADE)
#     payment_date = models.DateField()
#     payment_period = models.IntegerField()
#     payment_amount = models.DecimalField(max_digits=12, decimal_places=2)

#     def __str__(self):
#           return self.user.username


#     class Meta:
#         abstract = False
#         verbose_name = _("Payment")
#         verbose_name_plural = _("Payments")





class UserWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    currency = models.CharField(max_length=50, default='NGN')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.__str__()





class Discount(models.Model):
    value = models.IntegerField(default=0, verbose_name="Value")
    is_percentage = models.BooleanField(default=False, verbose_name="Is percentage?")

    def __str__(self):
        if self.is_percentage:
            return "{0}%".format(self.value)

        return "₦{0}".format(self.value)




class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, default='plan', max_length=60)
    plan_type = models.CharField(max_length=60)
    duration = models.CharField(max_length=24, choices=DURATION_CHOICES, default=DURATION_CHOICES[0][0])
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    coupon = models.ForeignKey(Coupon, related_name='payment_coupon', on_delete=models.CASCADE, blank=True, null=True)
    discount = models.ForeignKey(Discount, related_name='payment_discount', on_delete=models.CASCADE, blank=True, null=True)
    # discount = models.IntegerField(default=0, verbose_name="Discount Percentage", validators=[MinValueValidator(0), MaxValueValidator(100)])
    verified = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"


    # def get_discount_price(self):
    #     discount_price = self.amount * (self.discount / Decimal('100'))
    #     return  discount_price


    # def get_amount_payable(self):
    #     total_cost = self.amount - self.get_discount_price()
    #     return total_cost


    def get_amount_payable(self):
        if not self.coupon:
            return self.amount
        return self.coupon.get_discounted_value(self.amount)
        
    

    def amount_value(self):
        return Decimal(self.get_amount_payable()) * Decimal(100.00)
        # return Decimal(self.amount) * Decimal(100.00)
        # return int(self.amount) * 100


    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] /  Decimal(100.00) == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False


    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        # if self.coupon and not self.discount:
        #     self.
        super().save(*args, **kwargs)


