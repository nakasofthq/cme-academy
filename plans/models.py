from django.db import models
from django.conf import settings
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _
# from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save, post_delete

from cme.utils import unique_slug_generator, random_string_generator
from cme.decorators import PLAN_CHOICES, DURATION_CHOICES, FEE_STATUS
# from courses.models import Course




class Plan(models.Model):
    title = models.CharField(choices=PLAN_CHOICES, unique=True, max_length=30, default='free')
    slug = models.SlugField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, )
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True) 

    def __str__(self):
       return self.title


    class Meta:
        # abstract = False
        ordering = ("price",)


def plan_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(plan_pre_save_receiver, sender=Plan)



class UserPlan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_plan', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, related_name='user_plan', on_delete=models.SET_NULL, null=True) 
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)   

    def __str__(self):
       return "%s (%s)" %(self.user.username, self.plan.get_title_display())


    class Meta:
        ordering = ("created",)

    def get_user_grade(self):
        if self.plan.title == "free":
            grade = 0
        elif self.plan.title == "basic":
            grade = 1
        elif self.plan.title == "advance":
            grade = 2
        elif self.plan.title == "pro":
            grade = 3
        else:
            grade = 0
        return grade

    # def get_plan_courses(self):
    #     if self.plan.title == "free":
    #         qs = Course.objects.all().filter(level=0)
    #     elif self.plan.title == "basic":
    #         qs = Course.objects.all().filter(level__lte=1)
    #     elif self.plan.title == "advance":
    #         qs = Course.objects.all().filter(level__lte=2)
    #     elif self.plan.title == "pro":
    #         qs = Course.objects.all().filter(level__lte=3)
    #     else:
    #         qs = []
    #     return qs





class Subscription(models.Model):
    user_plan = models.ForeignKey(UserPlan, related_name='subscription', on_delete=models.CASCADE)
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
          return self.user_plan.user.username


    class Meta:
        abstract = False
        verbose_name = _("User Subscription")
        verbose_name_plural = _("User Subscriptions")
        ordering = ("created",)

    # def __str__(self):
    #     return "%s [%s - %s]" % (self.user.username, self.user_plan.plan, self.subscription_period)

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

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.pricing.name == 'Individual':
    #         self.policy.allow_dependant = False
    #         self.policy.save()
    #     elif self.pricing.name == 'Family':
    #         self.policy.allow_dependant = True
    #         self.policy.save()
    #     else:
    #         pass
    #     super().save(*args, **kwargs)












