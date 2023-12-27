from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.shortcuts import redirect

from gadgets.forms import *
from gadgets.models import *


def index_gad(request):
    search_query = request.GET.get('q', '')

    if search_query:
        serching_gad = Gadget.objects.filter(Q(brand_gadget__icontains=search_query) |
                                             Q(model_gadget__icontains=search_query) |
                                             Q(serial_gadget__icontains=search_query) |
                                             Q(master_gadget__icontains=search_query) |
                                             Q(telefon_master_gadget__icontains=search_query))
    else:
        serching_gad = Gadget.objects.all()

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

    context = {
        'gadgets': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'gadgets/gadgets.html', context)


class AddGadgets(View):
    def get(self, request):
        form_gad = GadgetForm()

        return render(request, 'gadgets/add_gadget.html', context={'form_gad': form_gad})

    def post(self, request):
        bound_form_gad = GadgetForm(request.POST)

        if bound_form_gad.is_valid():
            bound_form_gad.save()

            return redirect('gadgets')
        return redirect('dashboard')


# class EditGadgets(View):
#     def get(self, request, telefon_master_gadget):
#         gadget = Gadget.objects.get(telefon_master_gadget__iexact=telefon_master_gadget)
#         form_gad = GadgetForm(instance=gadget)
#         return render(request, 'gadgets/edit_gadget.html', context={'form': form_gad, 'gadget': gadget})
