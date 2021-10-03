from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import *

urlpatterns = [
    path('login/', obtain_auth_token ,name='login'),
    path('register/', registration_view ,name='register'),
    path('logout/', log_out_view ,name='logout'),
    
]
