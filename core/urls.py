
from django.contrib import admin
from django.urls import path,include
from .views import *
from  . import views

from core.forms import *
# app_name='core'
urlpatterns = [
    path('',home),
    path('accounts/login/',views.UserLogin,name='login'),
    path('accounts/register/',views.RegisterView.as_view(),name='register'),
    path('accounts/logout/',views.UserLogout,name='logout'),
    path('accounts/profile/',views.ProfileView.as_view(),name='profile'),
    

    # for blog 
    path("blog/",views.post_list,name='post_list1'),
    path("blog/<int:id>/",views.post_categories,name='post_category'),
    path('blog/addblog/',views.addBlog,name='addblog'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_details,name='post_detail'),
    # path('blog/categories/<slug:slug>/', views.post_categories, name="post_categories"),
    path('blog/share/<int:post_id>/',views.post_share,name='post_share'),

    


]

