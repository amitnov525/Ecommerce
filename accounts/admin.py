from django.contrib import admin
from accounts.models import MyUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class MyAdmin(UserAdmin):
    list_display=['id','email','username','first_name','last_name','data_joined','last_login','is_active']
    readonly_fields=('data_joined','last_login')
    ordering=('-data_joined',)
    fieldsets=()
    list_filter=()
    filter_horizontal=()
admin.site.register(MyUser,MyAdmin)

