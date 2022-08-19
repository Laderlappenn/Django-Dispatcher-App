from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pkey>', views.post, name='post')
]