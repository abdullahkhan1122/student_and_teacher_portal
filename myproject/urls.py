"""
URL configuration for myproject project.

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
from django.urls import path ,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "FLEXi Admin"
admin.site.site_title = "FLEXi Portal"
admin.site.index_title = "Welcome to FLEXi Portal"



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),  # Login URL
    path('student/', include('studentportal.urls')),  # Student portal URLs
    path('teacher/', include('teacherportal.urls')),  # Teacher portal URLs
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)