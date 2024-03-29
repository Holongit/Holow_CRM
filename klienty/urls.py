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

from django.urls import path


from klienty.views import *


urlpatterns = [
    path('', index_kli, name='klienty'),
    path('add_klient/', AddKlient.as_view(), name='add_klient'),
    path('kartka_klienta/<int:pk>', kartka_klienta, name='kartka_klienta'),
    path('add_gadget_serwis/<int:pk>', add_gadget_serwis, name='add_gadget_serwis'),
    path('kartka_klienta_z_bazy/<int:pk>', kartka_klienta_z_bazy, name='kartka_klienta_z_bazy'),
    path('klient_gadget_change/<int:gadget_id><str:klient_name>', klient_gadget_change, name='klient_gadget_change'),
    path('edit_klient/<int:pk>', edit_klient, name='edit_klient'),
    path('delete_klient/<int:pk>', delete_klient, name='delete_klient'),
    path('filters_klient_change/<str:status>', filters_klient_change, name='filters_klient_change'),
]

