"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
<<<<<<< HEAD
from django.conf import settings 
from django.views.generic.base import RedirectView

urlpatterns = [
    path(settings.HTTP_PREFIX, include([
        path('', RedirectView.as_view(url='plag/'), name='go-home'),
=======
from django.conf import settings

from plag.views import index

urlpatterns = [
    path(settings.HTTP_PREFIX, include([
        path('', index), # Defaults to plag home view
>>>>>>> f1b863e38be10f0dac4a25c7750e91df77a14e22
        path('plag/', include('plag.urls')),
        path('admin/', admin.site.urls),
    ]))
]
