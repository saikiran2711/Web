"""core URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import accounts.views as a_views
import  app.views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', a_views.login_user,name="login"),
    path('login/',a_views.login_user,name='login'),
    path('home/',app_views.home,name="home"),
    path('logout/',a_views.logout_user,name='logout'),
    path('register/',a_views.register,name='register'),
     path('register_user/',app_views.register_user,name="register_user"),
    path('authenticate_user/',app_views.authenticate_user,name="authenticate_user"),
    path('success/',app_views.success,name="success"),
    path('failure/',app_views.failure,name="failure"),
path('Success/',app_views.Success,name="Success"),
    path('Failure/',app_views.Failure,name="Failure"),
     path('web/',app_views.web,name="web"),
path('webAuth/',app_views.webAuth,name="webAuth"),
path('calender/',app_views.Calender,name="calender"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
