from django.urls import path
from . import views

urlpatterns = [
    path('', views.acts, name='acceptor'),
    path('<int:pkey>', views.accept, name='accept')
]