
from django.contrib import admin
from django.urls import path
from maily.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('analysis/', analysis, name='analysis'),
    path('analysis/require/', require, name='require'),
    path('analysis/require/result/', result, name='result'),
    path('analysis/require/result/checked', checked, name='checked'),

]
