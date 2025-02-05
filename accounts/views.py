from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm#, UserCreationForm
# from django.contrib.auth.models import auth
from django.shortcuts import render, redirect, get_object_or_404

from affiliates.models import UserAffiliate, Referee#, AffiliateSubscription
from payments.models import UserWallet
from plans.models import Plan, UserPlan, Subscription
from .forms import RegisterForm, UserLoginForm 
from .models import User


# #Anonymous required
# def anonymous_required(function=None, redirect_url=None):

#    if not redirect_url:
#        redirect_url = 'invoice:dashboard'

#    actual_decorator = user_passes_test(
#        lambda u: u.is_anonymous,
#        login_url=redirect_url
#    )

#    if function:
#        return actual_decorator(function)
#    return actual_decorator




# @anonymous_required
# def login(request):
#     context = {}
#     if request.method == 'GET':
#         form = UserLoginForm()
#         context['form'] = form
#         return render(request, 'accounts/login.html', context)

#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)

#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)

#             return redirect('invoice:dashboard')
#         else:
#             context['form'] = form
#             messages.error(request, 'Invalid Credentials')
#             return redirect('accounts:login')


#     return render(request, 'accounts/login.html', context)





# @login_required
# def logout(request):
#     auth.logout(request)
#     return redirect('accounts:login')









def register_view(request):
    ref_code = request.GET.get("ref")
    # if request.method == 'POST':
    form = RegisterForm(request.POST or None, initial={'referer_code': ref_code})
    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        phone = form.clean_phone()
        email = form.clean_email()
        gender = form.cleaned_data.get("gender")
        username = form.clean_username()
        password = form.clean()['password1']
        referer_code = form.cleaned_data.get('referer_code')
        # print('PASSWORD ',password)
        # CREATING NEW USER
        new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, phone=phone, gender=gender)
        if new_user:
            # CREATING A NEW USER FREE-PLAN
            free_plan = Plan.objects.get(slug='free')
            user_plan = UserPlan.objects.create(user=new_user, plan=free_plan)
            user_plan.save()      
            # CREATING A NEW USER SUBSCRIPTION
            user_subscription = Subscription()
            user_subscription.user_plan = user_plan
            user_subscription.save()
            # CREATING NEW USER WALLET
            UserWallet.objects.create(user=new_user)
            # # CREATING AFFILIATE USING REFERER-CODE
            if referer_code:
                user_affiliate = UserAffiliate.objects.all().filter(referer_code=referer_code).first()
                if user_affiliate:
                    ref = Referee(referee=new_user, referer=user_affiliate, referer_code=referer_code)
                    ref.save()
            messages.success(request, 'Account created successfully')
        return redirect("accounts:login")
    # else:
    #     form = RegisterForm(initial={'referer_code': ref})
    # if ref.exist():
    context = {
        "form": form,
        "ref": ref_code,
    }
    # context = {
    #     "form": form
    # }
    return render(request, "registration/register.html", context)





def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')   
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successfully') 
            # return redirect('payments:initiate_payment')
            return redirect('dashboard:home')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, "registration/login.html", context)





@login_required(login_url="accounts:login")
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
    # if request.method == "POST":
    #     logout(request)

    #     # CLEAR MESSAGES
    #     system_messages = messages.get_messages(request)
    #     for message in system_messages:
    #         # This iteration is necessary
    #         pass

    #     messages.success(request, 'You have logged out') 
    #     return redirect('accounts:login')
    # return render(request, "home.html", {})




 


