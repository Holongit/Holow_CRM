from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from gadgets.forms import GadgetForm
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

    if SetingsCRM.objects.get(pk=1).filter_gadget == 'WSZYSCY':
        gadget_in_serwis = Gadget.objects.all()
    if SetingsCRM.objects.get(pk=1).filter_gadget == 'W SERWISIE':
        gadget_in_serwis = Gadget.objects.filter(in_serwis=True)

    if search_query:
        serching_gad = gadget_in_serwis.filter(Q(brand_gadget__icontains=search_query) |
                                               Q(model_gadget__icontains=search_query) |
                                               Q(serial_gadget__icontains=search_query) |
                                               Q(master_gadget__icontains=search_query) |
                                               Q(id=search_query_int) |
                                               Q(telefon_master_gadget__icontains=search_query))
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

    context = {
        'filters': setings_filter,
        'gadgets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'gadgets/gadgets.html', context)


