from django import forms
# from .models import Contact
# from captcha.fields import ReCaptchaField

class ContactForm(forms.Form):
    firstname = forms.CharField(label='First Name', max_length=100)
    lastname = forms.CharField(label='Last Name', max_length=100)
    phone = forms.IntegerField(label='Phone')
    email = forms.EmailField(label='Email')
    # company = forms.CharField(label='company', max_length=100, required=False)
    subject = forms.CharField(label='subject', max_length=120, required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    captcha = forms.CharField(max_length=24)

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        if not captcha == '7':
            raise forms.ValidationError("Your answer is incorrect.")
        return captcha

    def clean_message(self):
        message = self.cleaned_data.get('message')
        num_words = len(message.split())
        if num_words < 4:
        	raise forms.ValidationError("Message is too short.")
        return message



# class QuoteRequestForm(forms.Form):
#     fullname = forms.CharField(label='Name', max_length=100)
#     phone = forms.IntegerField(label='Phone')
#     email = forms.EmailField(label='Email')
#     company = forms.CharField(label='company', max_length=100, required=False)
#     type_of_plan = forms.CharField(label='type_of_plan', max_length=120, required=True)
#     number_of_enrollee = forms.CharField(label='number_of_enrollee', max_length=120, required=True)
#     comment = forms.CharField(label='comment', widget=forms.Textarea)
#     captcha = forms.CharField(max_length=24)

#     def clean_captcha(self):
#         captcha = self.cleaned_data.get('captcha')
#         if not captcha == '11':
#             raise forms.ValidationError("Your answer is incorrect.")
#         return captcha

#     # def clean_comment(self):
#     #     comment = self.cleaned_data.get('comment')
#     #     num_words = len(comment.split())
#     #     if num_words < 2:
#     #         raise forms.ValidationError("Comment is too short.")
#     #     return comment








# class ProvidersRegistrationForm(forms.Form):
#     title = forms.CharField(label='Title', max_length=100)
#     firstname = forms.CharField(label='First Name', max_length=100)
#     lastname = forms.CharField(label='Last Name', max_length=100)
#     email = forms.EmailField(label='Email')
#     phone = forms.IntegerField(label='Phone')
#     phone2 = forms.IntegerField(label='Phone2')
#     hospital = forms.CharField(label='hospital', max_length=100, required=False)
#     hospital_date = forms.DateField(label='hospital_date', required=False)
#     address = forms.CharField(label='address', max_length=240, required=True)
#     city = forms.CharField(label='City', max_length=40, required=True)
#     lga = forms.CharField(label='L.G.A', max_length=40, required=True)
#     state = forms.CharField(label='state', max_length=40, required=True)
#     comment = forms.CharField(label='comment', widget=forms.Textarea)
#     captcha = forms.CharField(max_length=24)

#     def clean_captcha(self):
#         captcha = self.cleaned_data.get('captcha')
#         if not captcha == '13':
#             raise forms.ValidationError("Your answer is incorrect.")
#         return captcha

#     # def clean_comment(self):
#     #     comment = self.cleaned_data.get('comment')
#     #     num_words = len(comment.split())
#     #     if num_words < 2:
#     #         raise forms.ValidationError("Comment is too short.")
#     #     return comment
