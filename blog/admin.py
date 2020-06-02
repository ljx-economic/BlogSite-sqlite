from django.contrib import admin
from .models import BlogType,Blog,ReadNum

# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display=('type_name','author','id')
    ordering=('id',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('title','blog_type','author','readnum_function','created_time','last_update_time','id')
    ordering=('id',)
    
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display=('read_num','blog','id')
    ordering=('id',)