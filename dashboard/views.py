from django.shortcuts import render

from gadgets.models import *

def index_dash(request):
    gadget = Gadget.objects.first()
    qnt_gadgetsq = gadget.id

    context = {
        'qnt_gadgets': qnt_gadgetsq
    }

    return render(request, 'dashboard.html', context=context)