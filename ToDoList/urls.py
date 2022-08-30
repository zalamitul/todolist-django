"""ToDoList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from users.middleware.middleware import auth_middleware
from users import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('signup',views.signup),
    path('signin',views.signin),
    path('addtodo',auth_middleware(views.addtodo),name='addtodo'),
    path('alltodo',auth_middleware(views.all),name='alltodo'),
    path('completetodo',auth_middleware(views.completetodo)),
    path('deletetodo',auth_middleware(views.deletetodo)),
    path('updatetodo',auth_middleware(views.updatetodo)),
    path('logout',auth_middleware(views.logout)),
    path('homepage',auth_middleware(views.homepage),name='homepage')
]
