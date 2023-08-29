from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.projects, name='projects'),
    path('single_projects/<str:pk>/', views.single_projects, name='single_projects'),
    path('create-project/', views.create_project, name='create-project'),
    path('update-project/<str:pk>/', views.update_project, name='update-project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete-project'),
]