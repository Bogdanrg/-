from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('', convert_url, name='home'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('history/', HistoryView.as_view(), name='history'),
    path('logout/', logout_user, name='logout'),
    path('reurl/<int:url_pk>', get_reurl, name='reurl')
]
