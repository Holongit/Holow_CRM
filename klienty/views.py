from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from gadgets.models import Klient, Gadget



def index_kli(request):
    search_query = request.GET.get('q', '')

    if search_query:
        serching_kli = Gadget.objects.filter(Q(master_gadget__icontains=search_query) |
                                             Q(telefon_master_gadget__icontains=search_query))
    else:
        serching_kli = Gadget.objects.all()

    paginator = Paginator(serching_kli, 14)

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

    return render(request, 'klienty/klienty.html', context=context)
