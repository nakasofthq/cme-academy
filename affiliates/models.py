from __future__ import unicode_literals
from django.conf import settings
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from cme.utils import unique_slug_generator, random_string_generator

from cme.decorators import AFFILIATE_CHOICES, DURATION_CHOICES, FEE_STATUS




class Affiliate(models.Model):
    title = models.CharField(choices=AFFILIATE_CHOICES, unique=True, max_length=30, default='free')
    slug = models.SlugField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True) 

    def __str__(self):
       return self.title


def affiliate_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(affiliate_pre_save_receiver, sender=Affiliate)


class UserAffiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_affiliate')
    affiliate = models.ForeignKey(Affiliate, related_name='affiliate', on_delete=models.SET_NULL, null=True)
    referer_code = models.CharField(max_length=120, blank=True, null=True, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True) 

    def __str__(self):
        return f"{self.user.username}-{self.referer_code} ({self.affiliate})"

    class Meta:
        ordering = ['-created',]
        verbose_name = "Affiliate User"
        verbose_name_plural = "Affiliate Users"


    def create_code(self, *args, **kwargs):
        if self.referer_code is None:
            obj = 101010 + int(self.id)
            self.referer_code = str(obj)
        return self.referer_code
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if not self.referer_code:
    #         self.referer_code = 101010 + self.id
    #     super().save(*args, **kwargs)


    # @receiver(post_save, sender=Referer)
    # def save_referer(sender, instance, **kwargs):
    #     if not self.referer_code:
    #         self.referer_code = 101010 + self.id
    #     instance.user.save()


# def referer_post_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.referer_code:
#         instance.referer_code = 101010 + instance.id
#         print("===INSTANCE ID===", instance.id)
#         # instance.referer_code = random_string_generator(size=6)

# post_save.connect(referer_post_save_receiver, sender=UserAffiliate)





class AffiliateSubscription(models.Model):
    user_affiliate = models.ForeignKey(UserAffiliate, related_name='affiliate_subscription', on_delete=models.CASCADE)
    subscription_period = models.CharField(_('Subscription Period'), max_length=24, choices=DURATION_CHOICES, default=DURATION_CHOICES[0][0]) 
    start_date = models.DateField(_('Start Date'), default=None, blank=True, null=True, db_index=True)
    end_date = models.DateField(_('End Date'), default=None, blank=True, null=True, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fee_status = models.CharField(_('Fee Status'), max_length=24, choices=FEE_STATUS, default=FEE_STATUS[0][0])
    # stop = models.CharField(choices=STATUS, default='0', max_length=24)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True) 

    def __str__(self):
          return self.user_affiliate.user.username

    class Meta:
        ordering = ['-created',]
        verbose_name = "Affiliate Subscription"
        verbose_name_plural = "Affiliate Subscriptions"

    def is_active(self):
        return self.active

    def is_expired(self):
        if self.end_date is None:
            return False
        else:
            return self.end_date < date.today()

    def days_left(self):
        if self.end_date is None:
            return None
        else:
            return (self.end_date - date.today()).days




class Referee(models.Model):
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referee')
    referer = models.ForeignKey(UserAffiliate, on_delete=models.CASCADE, related_name='referer')
    referer_code = models.CharField(max_length=120, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True) 

    def __str__(self):
        return f"To: {self.referee} From: {self.referer_code}"

    class Meta:
        ordering = ['-created',]
        verbose_name = "Affiliate Referee"
        verbose_name_plural = "Affiliate Referees"

