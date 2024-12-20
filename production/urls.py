"""production URL Configuration

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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from .views import print_example
from account.views import login_page, dashboard_page, admin_page, monitoring_page, apps_page
from functools import partial 
from klaen.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('testing/',print_example, name='testing' ),
    path('', login_page, name='login'),
    path('account/', include('account.urls')),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('admin-dashboard/', admin_page, name='admin-dashboard'),
    path('klaen/', include('klaen.urls')),
    #============================================================
    # November Updated
    path('klaen/monitorings/', monitoring_page, name='klaen-monitoring-page'),
    path('apps/', apps_page, name='apps-page'),
    
    
    # path('/api/login/', partial(login_api, running=None), name='api-login')
    
    
]

urlpatterns += staticfiles_urlpatterns()
