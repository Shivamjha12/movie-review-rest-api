from django.contrib import admin
from django.urls import path, include
from API.api import views

urlpatterns = [
       # path('', views.home, name='home'),
       path('', include('API.api.urls')),


]