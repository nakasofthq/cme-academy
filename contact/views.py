from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect


from .forms import ContactForm#, QuoteRequestForm, ProvidersRegistrationForm
# from posts.models import Post, Tag


def contact(request):
    # queryset = Post.objects.active()
    c_form = ContactForm(request.POST or None)

    if request.method == "POST":
        if c_form.is_valid():
            form_fullname = c_form.cleaned_data.get("fullname")
            # form_lastname = c_form.cleaned_data.get("lastname")
            form_phone = c_form.cleaned_data.get("phone")
            form_email = c_form.cleaned_data.get("email")
            # form_company = c_form.cleaned_data.get("company")
            # form_subject = c_form.cleaned_data.get("subject")
            form_message = c_form.cleaned_data.get("message")

            subject = 'From cmetradingacademy.com (Contact Form):'  # %s %(form_subject)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['dsixnine@gmail.com']
            contact_message = "\n fullname: %s \n Phone: %s \n Email: %s \n\n Message: \n %s" %(
                form_fullname,
                form_phone,
                form_email,
                # form_company,
                # form_subject,
                form_message)

            send_mail(subject,
                contact_message,
                from_email,
                to_email,
                fail_silently=False)
            context = {
                # "object_list": queryset,
                "c_form": c_form,
            }
            return HttpResponseRedirect('/contact/sent/')
            # return render(request, "contact.html", context)

    form_fullname = request.POST.get('fullname', '')
    # form_lastname = request.POST.get('lastname', '')
    form_phone = request.POST.get('phone', '')
    form_email = request.POST.get('email', '')
    # form_company = request.POST.get('company', '')
    # form_subject = request.POST.get('subject', '')
    form_message = request.POST.get('message', '')

    context = {
        # "object_list": queryset,
        "c_form": c_form,
        "fullname": form_fullname,
        # "lastname": form_lastname,
        "phone": form_phone,
        "email": form_email,
        # "company": form_company,
        # "subject": form_subject,
        "message": form_message,
    }
    return render(request, "contact/contact.html", context)





def contact_sent(request):
    c_form = ContactForm(request.POST or None)
    # contact_title = 'Your message has been sent. Thank you!'
    context = {
        "c_form": c_form,
    }
    return render(request, "contact/contact-sent.html", context)





# def quote_request(request):
#     # queryset = Post.objects.active()
#     c_form = QuoteRequestForm(request.POST or None)

#     if request.method == "POST":
#         if c_form.is_valid():
#             form_firstname = c_form.cleaned_data.get("firstname")
#             form_phone = c_form.cleaned_data.get("phone")
#             form_email = c_form.cleaned_data.get("email")
#             form_company = c_form.cleaned_data.get("company")
#             form_type_of_plan = c_form.cleaned_data.get("type_of_plan")
#             form_number_of_enrollee = c_form.cleaned_data.get("number_of_enrollee")
#             form_comment = c_form.cleaned_data.get("comment")

#             subject = 'From greenfieldhmo.com (Quote Request): %s' %('Quote Request')
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = ['contact@greenfieldhmo.com']
#             contact_message = " firstname: %s \n Phone: %s \n Email: %s \n Company: %s \n Type of plan: %s \n Number of enrollee: %s \n\n Comment: \n %s" %(
#                 form_firstname,
#                 form_phone,
#                 form_email,
#                 form_company,
#                 form_type_of_plan,
#                 form_number_of_enrollee,
#                 form_comment)

#             send_mail(subject,
#                 contact_message,
#                 from_email,
#                 to_email,
#                 fail_silently=False)
#             context = {
#                 # "object_list": queryset,
#                 "c_form": c_form,
#             }
#             return HttpResponseRedirect('/contact/message-sent/')
#             # return render(request, "contact.html", context)

#     form_firstname = request.POST.get('firstname', '')
#     form_phone = request.POST.get('phone', '')
#     form_email = request.POST.get('email', '')
#     form_company = request.POST.get('company', '')
#     form_type_of_plan = request.POST.get('type_of_plan', '')
#     form_number_of_enrollee = request.POST.get('number_of_enrollee', '')
#     form_comment = request.POST.get('comment', '')

#     context = {
#         # "object_list": queryset,
#         "c_form": c_form,
#         "firstname": form_firstname,
#         "phone": form_phone,
#         "email": form_email,
#         "company": form_company,
#         "type_of_plan": form_type_of_plan,
#         "number_of_enrollee": form_number_of_enrollee,
#         "comment": form_comment,
#     }
#     return render(request, 'home/contact/quote-request.html', context)






# # PROVIDER REGISTRATION

# def providers_registration(request):
#     # queryset = Post.objects.active()
#     c_form = ProvidersRegistrationForm(request.POST or None)

#     if request.method == "POST":
#         if c_form.is_valid():
#             form_title = c_form.cleaned_data.get("title")
#             form_firstname = c_form.cleaned_data.get("firstname")
#             form_lastname = c_form.cleaned_data.get("lastname")
#             form_email = c_form.cleaned_data.get("email")
#             form_phone = c_form.cleaned_data.get("phone")
#             form_phone2 = c_form.cleaned_data.get("phone2")
#             form_hospital = c_form.cleaned_data.get("hospital")
#             form_hospital_date = c_form.cleaned_data.get("hospital_date")
#             form_address = c_form.cleaned_data.get("address")
#             form_city = c_form.cleaned_data.get("city")
#             form_lga = c_form.cleaned_data.get("lga")
#             form_state = c_form.cleaned_data.get("state")
#             form_comment = c_form.cleaned_data.get("comment")

#             subject = 'From greenfieldhmo.com (Provider Reg.): %s' %('Provider Registration')
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = ['contact@greenfieldhmo.com']
#             contact_message = " Title: %s \n Full firstname: %s %s \n Phone: %s \n Mobile: %s \n Email: %s \n Hospital firstname: %s \n Hospital Date of Establishment: %s \n Address: %s \n City: %s \n L.G.A: %s \n State: %s \n\n Comment: \n %s" %(
#                 form_title,
#                 form_firstname,
#                 form_lastname,
#                 form_phone,
#                 form_phone2,
#                 form_email,
#                 form_hospital,
#                 form_hospital_date,
#                 form_address,
#                 form_city,
#                 form_lga,
#                 form_state,
#                 form_comment)

#             send_mail(subject,
#                 contact_message,
#                 from_email,
#                 to_email,
#                 fail_silently=False)
#             context = {
#                 # "object_list": queryset,
#                 "c_form": c_form,
#             }
#             return HttpResponseRedirect('/contact/providers/registration/sent/')
#             # return render(request, "contact.html", context)

#     form_title = request.POST.get('title', '')
#     form_firstname = request.POST.get('firstname', '')
#     form_lastname = request.POST.get('lastname', '')
#     form_email = request.POST.get('email', '')
#     form_phone = request.POST.get('phone', '')
#     form_phone2 = request.POST.get('phone2', '')
#     form_hospital = request.POST.get('hospital', '')
#     form_hospital_date = request.POST.get('hospital_date', '')
#     form_address = request.POST.get('address', '')
#     form_city = request.POST.get('city', '')
#     form_lga = request.POST.get('lga', '')
#     form_state = request.POST.get('state', '')
#     form_comment = request.POST.get('comment', '')

#     context = {
#         # "object_list": queryset,
#         "c_form": c_form,
#         "title": form_title,
#         "firstname": form_firstname,
#         "lastname": form_lastname,
#         "email": form_email,
#         "phone": form_phone,
#         "phone2": form_phone2,
#         "hospital": form_hospital,
#         "hospital_date": form_hospital_date,
#         "address": form_address,
#         "city": form_city,
#         "lga": form_lga,
#         "state": form_state,
#         "comment": form_comment,
#     }
#     return render(request, 'home/contact/providers-registration.html', context)







# def providers_registration_sent(request):
#     c_form = ContactForm(request.POST or None)
#     # contact_title = 'Your message has been sent. Thank you!'
#     context = {
#         "c_form": c_form,
#     }
#     return render(request, "home/contact/providers-registration-sent.html", context)




