from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [

    path('register/',views.register,name='register'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logoutuser, name="logout"),
]