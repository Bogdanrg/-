from django.urls import path, include
from .views import *


urlpatterns = [
    path('', convert_url, name='home'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('history/', HistoryView.as_view(), name='history'),
    path('logout/', logout_user, name='logout')
]
