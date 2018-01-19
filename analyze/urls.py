from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_project, name='create'),
    path('report/<int:project_id>/', views.report_project, name='report'),
]

