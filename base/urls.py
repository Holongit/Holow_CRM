"""
URL configuration for base project.

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
from django.urls import path

import gadgets.views
from dashboard.views import index_dash
from gadgets.views import *
from klienty.views import index_kli

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_dash, name='dashboard'),
    path('klienty/', index_kli, name='klienty'),
    path('add_gadget/', AddGadgets.as_view(), name='add_gadget'),
    path('gadgets/', index_gad, name='gadgets'),
    path('gadgets/edit_gadget/<int:pk>/', EditGadget.as_view(), name='edit_gadget'),
    path('gadgets/delete_gadget/<int:pk>/', delete_gadget, name='delete_gadget'),
    path('gadgets/gadget_status_change/<int:pk><str:status>/', gadget_status_change, name='gadget_status_change'),
    path('gadgets/service_status_change/<int:pk><str:status>/', service_status_change, name='service_status_change'),
    path('gadgets/outgo_gadget/<int:pk>/', OutgoGadget.as_view(), name='outgo_gadget'),
    path('gadgets/filters/<str:status>/', filters_gadget_change, name='filters_gadget_change'),
]

