"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/user/register/', views.api_register_user, name='user-reg'), #POST создание нового пользователя
    # path('api/user/login/', views.api_login_user, name='user-login'), #POST залогиниться
    # path('api/user/<int:pk>/', views.api_info_user, name='user-private'), #PUT личный кабинет
    # path('api/user/<int:pk>/create_org/', views.create_user, name='user-whoami'),

    path('user/login/', views.login_user, name='user-login'), 
    path('user/login/check/', views.check_login_user, name='user-login'),
    path('user/register/', views.register_user, name='user-login'),
    path('user/register/check/', views.check_register_user, name='user-login'),
    path('user/<int:pk>/accaunt/', views.accaunt_user, name='user-login'), 
    path('user/<int:pk>/accaunt/clicked_ld/', views.clicked_ld_accaunt_user, name='user-login'),  
    path('user/<int:pk>/accaunt/logout/', views.logout_accaunt_user, name='user-login'),  
    path('user/<int:pk>/create_event/', views.create_event, name='event_creation'),
    path('user/<int:pk>/create_event/check/', views.check_create_event, name='event_creation'),


    path('home/', views.home, name='user-whoami'),
    # path('home/<int:pk>/info/', views.info_org_home, name='user-whoami'),

]
