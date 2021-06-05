"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('property/', views.get_property.as_view(), name='property'),
    path('propertytax/<int:id>', views.get_PropertyTax.as_view(), name='getpropertytax'),
    path('', views.home, name='home'),
    path('dashboardview', views.dashboard, name='dashboardview'),
    path('propsearch', views.propsearch, name='propsearch'),
    path('dashboard/', views.get_Dashboard_Data.as_view(), name='dashboard'),

    # path('', views.home, name='home'),
    # path('table', views.table, name='table'),
    # path('index/', views.index, name='index'),
]