from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from OPUSSerwis20.models import *


@login_required(login_url='login')
def index_opusserwis20(request):
    search_query = request.GET.get('q', '')

    if search_query:
        serching_opus = NaprawyOpus.objects.filter(Q(KNP_NR_WLASCICIELA__name_klient__icontains=search_query) |
                                                  Q(KNP_NR_WLASCICIELA__telefon_klient__icontains=search_query) |
                                                  Q(KNP_PRD_ID__PRD_NAZWA__icontains=search_query) |
                                                  Q(KNP_NR_SER_KOL__icontains=search_query))
    else:
        serching_opus = NaprawyOpus.objects.all()
    paginator = Paginator(serching_opus, 50)
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


    context = {
        'klients': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'OPUSSerwis20/OPUSSerwis20.html', context=context)

@login_required(login_url='login')
def kartka_naprawy(request, pk):

    if request.method == 'GET':
        naprawa_opus = NaprawyOpus.objects.get(pk=pk)

        return render(request, 'OPUSSerwis20/kartka_naprawy.html', context={'naprawa_opus': naprawa_opus})
