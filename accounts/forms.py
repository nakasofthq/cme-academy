from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django_select2.forms import Select2MultipleWidget
from django_select2 import forms as s2forms
# from pagedown.widgets import PagedownWidget

# from newsletter.models import Newsletter
from plans.models import Plan, UserPlan, Subscription
from affiliates.models import UserAffiliate
from .models import *





class RegisterForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20, validators=[UnicodeUsernameValidator()], help_text='This cannot be changed.')
    first_name = forms.CharField(max_length=25, label="First Name")
    last_name = forms.CharField(max_length=25, label="Last Name")
    phone = forms.CharField(label=_("Phone:"),
                       # required = True,
                       help_text = 'Only you can see your phone number.',
                       widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "08012345678"}),)
    email = forms.EmailField(label="Email")
    gender = forms.CharField(label=_("Gender:"),
                       # required = True,
                       # help_text = 'Only you can see your phone number.',
                       widget=forms.Select(choices=GENDERS, attrs={"class": "form-control"}),)
    referer_code = forms.CharField(max_length=25, label="Referer Code", required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        # qs = User.objects.filter(username__iexact=username)
        # if qs.exists():
        if username and User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Username is taken")
        return username.lower()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        qs = User.objects.filter(phone__iexact=phone)
        if qs.exists():
            raise ValidationError("Phone is taken")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise ValidationError("Email is taken")
        return email

    def clean(self):
        data = super(RegisterForm, self).clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not password1 or not password2:
            raise ValidationError("Passwords must match.")
        elif password1 != password2:
            raise ValidationError("Passwords must match.")
        referer_code = self.cleaned_data['referer_code']
        qs = UserAffiliate.objects.filter(referer_code=referer_code)
        if referer_code and not qs.exists():
            raise ValidationError("Invalid Affiliate Referer Code")
        return data

    # def clean_referer(self):
    #     ref = self.cleaned_data['referer_code']
    #     qs = UserAffiliate.objects.filter(referer_code=ref)
    #     if not qs.exists():
    #         raise forms.ValidationError("Invalid Referer Code")
    #     return ref





# class SignUpForm(UserCreationForm):
#     free_plan = Plan.objects.get(plan_type='Free')

#     class Meta(UserCreationForm.Meta):
#        model = User    

#        def save(self):
#           user = super().save(commit=False)
#           user.save()
#           # Creating a new UserPlan
#           user_plan = UserPlan.objects.create(user=user, plan=self.free_plan)
#           user_plan.save()      
#           # Creating a new UserSubscription
#           user_subscription = Subscription()
#           user_subscription.user_plan = user_plan
#           user_subscription.save()
#           return user








class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
                            widget=forms.TextInput(attrs={'id': 'floatingInput', 'class': 'form-control mb-3'}),
                            required=True)
    password = forms.CharField(
                            widget=forms.PasswordInput(attrs={'id': 'floatingPassword', 'class': 'form-control mb-3'}),
                            required=True)

    class Meta:
        model=User
        fields=['username','password']







