from django.urls import path
from . import views, views_htmx

urlpatterns = [
    path('', views.acts, name='acts'),
    path('create/', views.create_act, name='create_act'),
    path('<int:pkey>/', views.act, name='act'),
    path('search',views.act_search),

    path('<int:pkey>/edit/', views_htmx.act_edit_form, name='act-edit-form'),
    path('<int:pkey>/edit/save', views_htmx.act_edit),
    path('status/', views_htmx.act_status),
]