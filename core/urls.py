"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'),  namespace='accounts')),
    path('acts/', include(('acts.urls', 'acts'))),
    path('', include(('main.urls', 'main'),  namespace='main')),
    path('reports/', include(('reports.urls', 'reports'),  namespace='reports')),
    path('coordinations/', include(('coordinator.urls', 'cordinations'),  namespace='coordinations')),
    path('accept/', include(('acceptor.urls', 'acceptions'),  namespace='acceptions')),
    path('__debug__/', include('debug_toolbar.urls')),
]
