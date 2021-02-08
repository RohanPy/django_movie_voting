from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [


    path('register/',views.RegisterView.as_view(),name='register'),
    # login
    path('login/',auth_views.LoginView.as_view(),name='login'),
    # logout
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),




]