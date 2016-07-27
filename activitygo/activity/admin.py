from django.contrib import admin
from activity.models import User, Activities

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	fields = ('username', 'credit')
	list_display = ('username', 'phone', 'email', 'credit')

def change_status_to_1(self, request, queryset):
	rowupdate = queryset.update(astatus = 1)

def change_status_to_0(self, request, queryset):
	rowupdate = queryset.update(astatus = 0)


class ActivitiesAdmin(admin.ModelAdmin):
	fields = ('aname', 'adate', 'alocation', 'aorganiser','aparticipantnum', 'astatus')
	list_display = ('aname', 'adate', 'alocation',  'aorganiser', 'astatus')
	actions = [change_status_to_1, change_status_to_0]



change_status_to_0.short_description = "change selected activities status to 0"
change_status_to_1.short_description = "change selected activities status to 1"


admin.site.register(User, UserAdmin)
admin.site.register(Activities, ActivitiesAdmin)