from django.contrib import admin
from activity.models import User, Activities

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	fields = ('username', 'credit')
	list_display = ('username', 'phone', 'email', 'credit')

class ActivitiesAdmin(admin.ModelAdmin):
	fields = ('aname', 'adate', 'alocation', 'aorganiser', 'astatus')
	list_display = ('aname', 'adate', 'alocation', 'aorganiser', 'astatus')

admin.site.register(User, UserAdmin)
admin.site.register(Activities, ActivitiesAdmin)