from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from workers.models import Workers


def workers(request):
    worker = Workers.objects.all()
    group = User.objects.last()

    return render(request, 'workers/workers.html', {'pracowniki': worker, 'users': group})
