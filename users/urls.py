from django.urls import path, include
from users.views import login

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]