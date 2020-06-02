from django.urls import path
from . import views

urlpatterns=[
    path('update_comment',views.update_comment,name='update_comment'),
    path('manage/',views.comment_manage,name='comment_manage'),
    path('change/<int:comment_pk>',views.comment_change,name='comment_change'),
    path('delete/<int:comment_pk>',views.comment_delete,name='comment_delete'),
]