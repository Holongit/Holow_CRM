from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from gadgets.models import Gadget, SetingsCRM
from workers.models import Workers



def workers(request):
    users = User.objects.all()

    return render(request, 'workers/workers.html', {'users': users})

@login_required(login_url='login')
def workers_gad_list(request, pk):
    search_query = request.GET.get('q', '')
    if search_query.isnumeric():
        search_query_int = int(search_query)
    else:
        search_query_int = 0

    if SetingsCRM.objects.get(pk=1).filter_work == 'WSZYSCY':
        gadget_in_serwis = Workers.objects.filter(worker=pk)

    if SetingsCRM.objects.get(pk=1).filter_work == 'W SERWISIE':
        gadget_in_serwis = Workers.objects.filter(worker=pk, gadget__in_serwis=True)

    if search_query:
        serching_gad = gadget_in_serwis.filter(Q(gadget__brand_gadget__icontains=search_query) |
                                               Q(gadget__model_gadget__icontains=search_query) |
                                               Q(gadget__serial_gadget__icontains=search_query) |
                                               Q(gadget__master_gadget__icontains=search_query) |
                                               Q(gadget__id=search_query_int) |
                                               Q(gadget__telefon_master_gadget__icontains=search_query))
    else:
        serching_gad = gadget_in_serwis

    paginator = Paginator(serching_gad, 14)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    setings_filter = SetingsCRM.objects.get(pk=1)

    user = User.objects.get(id=pk)

    context = {
        'filters': setings_filter,
        'gadgets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'user': user,
    }

    return render(request, 'workers/worker_gad_list.html', context)

@login_required(login_url='login')
def filters_work_change(request, status):
    setings_f = get_object_or_404(SetingsCRM.objects.all(), pk=1)
    setings_f.filter_work = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))

@method_decorator(login_required(login_url='login'), name='dispatch')
class GadgetInfo(View):
    def get(self, request, pk, user_pk):
        gadget = Gadget.objects.get(id=pk)
        notes = gadget.note_set.all()
        return render(request, 'workers/gadget_info.html', context={'gadget': gadget, 'notes': notes, 'user_pk': user_pk})

    def post(self, request, pk):
        gadget = Gadget.objects.get(id=pk)
        if gadget.in_serwis:
            gadget.in_serwis = False
            gadget.save()
        elif not gadget.in_serwis:
            gadget.in_serwis = True
            gadget.save()
        return redirect(request.META.get('HTTP_REFERER'))

def add_gadget_to_worker(request, pk):
    user = request.user
    gadget = Gadget.objects.get(id=pk)
    if gadget.in_serwis:
        if Workers.objects.filter(gadget__id=pk).exists():
            s = Workers.objects.get(gadget__id=pk)
            s.updated_at = timezone.now()
            s.worker = user
            s.save()
        else:
            Workers.objects.create(worker=user, gadget=gadget)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


def delete_gadget_to_worker(request, pk):
    worker = Workers.objects.filter(gadget__id=pk)
    worker.delete()
    return redirect(request.META.get('HTTP_REFERER'))