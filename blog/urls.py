from django.urls import path
from . import views

urlpatterns=[
    path('<username>',views.blog_list,name='blog_list'),
    path('articles/<int:blog_pk>',views.blog_detail,name='blog_detail'),
    path('type/<int:blog_type_pk>',views.blogs_with_type,name='blogs_with_type'),
    path('manage/',views.blog_manage,name='blog_manage'),
    path('add/',views.blog_add,name='blog_add'),
    path('change/<int:blog_pk>',views.blog_change,name='blog_change'),
    path('delete/<int:blog_pk>',views.blog_delete,name='blog_delete'),
    path('blog_type/manage/',views.blog_type_manage,name='blog_type_manage'),
    path('blog_type/add/',views.blog_type_add,name='blog_type_add'),
    path('blog_type/change/<int:blog_type_pk>',views.blog_type_change,name='blog_type_change'),
    path('blog_type/delete/<int:blog_type_pk>',views.blog_type_delete,name='blog_type_delete'),
]