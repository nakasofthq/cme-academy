from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _ 
from accounts.models import User, GENDERS
from .models import HelpCenter#, Contact


User = get_user_model()



#forms.py
class ProfileForm(forms.ModelForm):
    username = forms.CharField(label=_("Username"),
                                required = True,
                                min_length=5, 
                                max_length=20,
                                validators=[UnicodeUsernameValidator()],
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label=_("First Name"),
                                required = True,
                                max_length=25,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_("Last Name"),
                                required = True,
                                max_length=25,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label=_("Phone:"),
                               # required = True,
                               help_text = 'Only you can see your phone number.',
                               widget=forms.TextInput(attrs={"class": "form-control"}),)
    email = forms.CharField(label=_("Email address:"),
                               max_length=50,
                               required = True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    gender = forms.CharField(label=_("Gender:"),
                                           required = True,
                                           widget=forms.Select(choices=GENDERS, attrs={'class': 'form-control select2'}))
    address = forms.CharField(label=_("Address"),
                               required = True,
                               help_text='Enter your full physical address',
                               widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'gender', 'address']





class HelpCenterForm(forms.ModelForm):
    subject = forms.CharField(label=_("Subject"),
                                required = True,
                                max_length=120,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label=_("Message"),
                                required = True,
                                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),)
    
    class Meta:
        model = HelpCenter
        fields = ['subject', 'message',]

    def clean_message(self):
        message = self.cleaned_data.get('message')
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Message is too short.")
        return message







# class ContactForm(forms.ModelForm):
#     last_name = forms.CharField(label=_('Last Name'),
#                                 required = True,
#                                 max_length=60,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     first_name = forms.CharField(label=_('First Name'),
#                                 required = True,
#                                 max_length=60,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     phone = forms.IntegerField(label=_('Phone'),
#                                 required = True,
#                                 # max_length=120,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label=_('Email'),
#                                 required = True,
#                                 max_length=60,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     company = forms.CharField(label=_('Company'),
#                                 required = False,
#                                 max_length=120,
#                                 help_text= 'If you are from a corporate partner.',
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     subject = forms.CharField(label=_("Subject"),
#                                 required = True,
#                                 max_length=120,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     message = forms.CharField(label=_("Message"),
#                                 required = True,
#                                 widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),)
#     captcha = forms.CharField(label=_("Enter answer below: 3 + 4 = ?"),
#                                 required = True,
#                                 max_length=12,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = Contact
#         fields = ['last_name', 'first_name', 'phone', 'email', 'company', 'subject', 'message', 'captcha',]


#     def clean_captcha(self):
#         captcha = self.cleaned_data.get('captcha')
#         if not captcha == '7':
#             raise forms.ValidationError("Your answer is incorrect.")
#         return captcha

#     def clean_message(self):
#         message = self.cleaned_data.get('message')
#         num_words = len(message.split())
#         if num_words < 4:
#             raise forms.ValidationError("Message is too short.")
#         return message











