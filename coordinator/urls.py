from django.urls import path
from . import views

urlpatterns = [
    path('random_name_page/', views.random_name_page, name='random_name_page'),
    path('random_name/', views.random_name, name='random_name'),


]