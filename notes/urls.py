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

from notes.views import NoteAdd, delete_note,red_note



urlpatterns = [
    path('add_note/<int:pk>/', NoteAdd.as_view(), name='add_note'),
    path('delete_note/<int:pk>/', delete_note, name='delete_note'),
    path('read_note/<int:pk>/', red_note, name='red_note'),
]

