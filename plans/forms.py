# ### import datetimefrom django import forms
# from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
# from membership.models import Plan, UserPlan, Subscription




# class SignUpForm(UserCreationForm):
#     free_plan = Plan.objects.get(title='Free')    

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


