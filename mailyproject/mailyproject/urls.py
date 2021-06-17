"""mailyproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from maily.views import *


urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('login/report/', report, name='report'),
    path('login/report/delete/', delete, name='delete'),
    path('login/report/delete/confirm', confirm, name='confirm'),
    path('login/report/delete/result/', result, name='result'),
]
