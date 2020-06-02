from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('forget/',views.forget,name='forget'),
    path('code/',views.ve_code,name='code'),
    path('change_password/',views.change_password,name='change_password'),
    path('change/',views.change,name='change'),
    path('change_info/',views.change_info,name='change_info'),
]