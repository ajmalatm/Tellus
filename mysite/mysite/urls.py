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
from django.contrib.auth import views as auth_views
from register import views as v


admin.site.site_header='TELLUS'
admin.site.site_title='TELLUS'
admin.site.index_title='TELLUS Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', v.register, name='register'),
    path('login/', v.loginPage, name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='reset_password_sent'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),

    path('tellus/', include('tellus.urls')),
    path('', include('tellus.urls')),
    path('map/', include('map.urls')),
    path('', include('django.contrib.auth.urls')),
]
