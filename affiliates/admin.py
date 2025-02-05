from django.contrib import admin
from .models import Affiliate, UserAffiliate, AffiliateSubscription, Referee

# Register your models here.





class AffiliateAdmin(admin.ModelAdmin):
    list_display  = ["id", "title", "slug", 'price']
    list_filter = ["created", "updated",]
    search_fields = ['title']
    ordering = ['price']

    class Meta:
        model = Affiliate

admin.site.register(Affiliate, AffiliateAdmin) 



class UserAffiliateAdmin(admin.ModelAdmin):
    list_display = ["user", "referer_code"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "referer_code"]
    list_filter = ["created", "updated"]

    class Meta:
        model = UserAffiliate

admin.site.register(UserAffiliate, UserAffiliateAdmin) 



class AffiliateSubscriptionAdmin(admin.ModelAdmin):
    list_display  = ["id", "user_affiliate", "subscription_period", "start_date", "end_date", 'amount', "fee_status", "active", "updated", "created"]
    list_filter = ["created", "updated", "active", "fee_status", "start_date", "end_date", "subscription_period",]
    search_fields = ['user_affiliate__user__username', 'user_affiliate__user__first_name', 'user_affiliate__user__last_name', 'user_affiliate__plan__title']
    ordering = ['-created',]

    class Meta:
        model = AffiliateSubscription

admin.site.register(AffiliateSubscription, AffiliateSubscriptionAdmin) 



class RefereeAdmin(admin.ModelAdmin):
    list_display = ["referee", "referer", "referer_code"]
    search_fields = ["referee__user_affiliate__user__username", "referer_code"]
    list_filter = ["created", "updated"]

    class Meta:
        model = Referee

admin.site.register(Referee, RefereeAdmin) 

