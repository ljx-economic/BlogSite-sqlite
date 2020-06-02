from django.contrib import admin
from .models import UserInfo

# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display=('user','code','introduction','id')
    ordering=('id',)