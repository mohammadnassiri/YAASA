from django.contrib import admin
from django.urls import path, include

from apksa import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', include('analyze.urls')),
    path('admin/', admin.site.urls),
]