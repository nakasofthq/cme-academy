from django.contrib import admin

from .models import HelpCenter




class HelpCenterAdmin(admin.ModelAdmin):	
	list_display = ['user', 'subject', 'timestamp']
	list_filter = ['timestamp',]
	search_fields = ['message', 'user', 'subject']

	class Meta:
		model = HelpCenter

admin.site.register(HelpCenter, HelpCenterAdmin)
