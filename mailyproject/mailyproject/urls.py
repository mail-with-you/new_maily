
from django.contrib import admin
from django.urls import path
from maily.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('report/', report, name='report'),
    path('report/delete/', delete, name='delete'),
    # path('report/require/result/', result, name='result'),
    # path('report/require/result/checked', checked, name='checked'),

]
