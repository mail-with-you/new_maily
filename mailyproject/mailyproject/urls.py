
from django.contrib import admin
from django.urls import path
from maily.views import *


urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('login/report/', report, name='report'),
    path('login/report/delete/', delete, name='delete'),
    # path('report/require/result/', result, name='result'),
    # path('report/require/result/checked', checked, name='checked'),

]
