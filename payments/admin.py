from django.contrib import admin
from .models import Payment, UserWallet, Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


class PaymentAdmin(admin.ModelAdmin):
	list_display  = ["id", "ref", "user", 'amount', "category", "plan_type", "duration", "verified", "date_created"]
	list_filter = ['verified', 'date_created', 'updated', 'category', 'plan_type', 'duration']
	search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']

admin.site.register(Payment, PaymentAdmin)


# class UserWalletAdmin(admin.ModelAdmin):
# 	list_display  = ["id", "user", 'currency', "balance", "updated", "date_created"]

# admin.site.register(UserWallet, UserWalletAdmin)