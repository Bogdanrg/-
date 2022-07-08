from django.urls import path, include
from .views import *


urlpatterns = [
    path('', convert_url, name='home'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('login/', login, name='login'),
    path('history/', history, name='history')
]
