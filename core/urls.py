
from django.contrib import admin
from django.urls import path,include
from .views import *
from  . import views

from core.forms import *
urlpatterns = [
    path('',home),
    path('accounts/login/',views.UserLogin,name='login'),
    path('accounts/register/',views.RegisterView.as_view(),name='register'),
    path('accounts/logout/',views.UserLogout,name='logout'),
    path('accounts/profile/',views.ProfileView.as_view(),name='profile'),
    

    


]

