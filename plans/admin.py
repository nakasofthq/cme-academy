from django.contrib import admin
from .models import Plan, UserPlan, Subscription


class PlanAdmin(admin.ModelAdmin):
    list_display  = ["id", "title", "slug", 'price']
    list_filter = ["created", "updated", 'title']
    ordering = ['price',]

class UserPlanAdmin(admin.ModelAdmin):
    list_display  = ["id", "user", "plan", "updated", "created"]
    list_filter = ["created", "updated", 'plan__title']
    # ordering = ['-created',]

class SubscriptionAdmin(admin.ModelAdmin):
    list_display  = ["id", "user_plan", "subscription_period", "start_date", "end_date", 'amount', "fee_status", "active", "updated", "created"]
    list_filter = ["created", "updated", "active", "fee_status", "start_date", "end_date", "subscription_period",]
    search_fields = ['user_plan__user__username', 'user_plan__user__first_name', 'user_plan__user__last_name', 'user_plan__plan__title']
    ordering = ['-created',]

admin.site.register(Plan, PlanAdmin)
admin.site.register(UserPlan, UserPlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)