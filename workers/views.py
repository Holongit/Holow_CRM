from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone

from gadgets.models import Gadget, SetingsCRM
from workers.models import Workers, KartkaPlatne, KartkaGwarancja, KartkaReklamacja, KartkaRezygnacja
from notes.models import Note
from notes.form import NoteForm
from gadgets.forms import OpisNaprawyForm


@login_required(login_url='login')
def workers(request):
    users = User.objects.all()

    return render(request, 'workers/workers.html', {'users': users})


@login_required(login_url='login')
def workers_gad_list(request, pk):
    global gadget_in_serwis
    user = request.user
    search_query = request.GET.get('q', '')
    date_range = request.GET.get('date_range', '')
    if search_query.isnumeric():
        search_query_int = int(search_query)
    else:
        search_query_int = 0

    date_one = date_range[:10]
    date_two = date_range[14:]

    if not SetingsCRM.objects.filter(user_id=user.id).exists():
        SetingsCRM.objects.create(user_id=user.id)

    if date_range:
        date_one_date_time_obj = datetime.strptime(date_one, '%Y-%m-%d')
        date_two_date_time_obj = datetime.strptime(date_two, '%Y-%m-%d')
        gadget_date_range = Workers.objects.filter(added_at__gt=date_one_date_time_obj,
                                                   added_at__lt=date_two_date_time_obj,
                                                   worker=pk,
                                                   )
        if SetingsCRM.objects.get(user_id=user.id).filter_work == 'WSZYSCY':
            gadget_in_serwis = gadget_date_range

        if SetingsCRM.objects.get(user_id=user.id).filter_work == 'W SERWISIE':
            gadget_in_serwis = gadget_date_range.filter(worker=pk,
                                                        in_work=True,
                                                        )
    else:
        if SetingsCRM.objects.get(user_id=user.id).filter_work == 'WSZYSCY':
            gadget_in_serwis = Workers.objects.filter(worker=pk)

        if SetingsCRM.objects.get(user_id=user.id).filter_work == 'W SERWISIE':
            gadget_in_serwis = Workers.objects.filter(worker=pk,
                                                      in_work=True,
                                                      )

    if len(str(search_query_int)) <= 5 and search_query_int > 0:
        serching_gad = gadget_in_serwis.filter(gadget__id=search_query_int)

    elif search_query:
        serching_gad = gadget_in_serwis.filter(Q(gadget__brand_gadget__icontains=search_query) |
                                               Q(gadget__model_gadget__icontains=search_query) |
                                               Q(gadget__serial_gadget__icontains=search_query) |
                                               Q(gadget__klient__name_klient__icontains=search_query) |
                                               Q(gadget__klient__telefon_klient__icontains=search_query) |
                                               Q(gadget__password_gadget__icontains=search_query))
    else:
        serching_gad = gadget_in_serwis

    paginator = Paginator(serching_gad, 40)

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

    setings_filter = SetingsCRM.objects.get(user_id=user.id)

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
    user = request.user
    setings_f = get_object_or_404(SetingsCRM.objects.all(), user_id=user.id)
    setings_f.filter_work = status
    setings_f.save()
    return redirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required(login_url='login'), name='dispatch')
class GadgetInfo(View):
    def get(self, request, pk):
        gadget = Gadget.objects.get(id=pk)
        notes = gadget.note_set.all()
        form_note = NoteForm(initial={'title': 'none'})
        form_opis = OpisNaprawyForm(initial={'opis_naprawy': gadget.opis_naprawy})
        context = {'gadget': gadget,
                   'notes': notes,
                   'form': form_note,
                   'form_opis': form_opis,
                   }
        return render(request, 'workers/gadget_info.html', context=context)

    def post(self, request, pk):
        bound_form_note = NoteForm(request.POST)
        gadget_id = Gadget.objects.get(id=pk)
        user_id = request.user

        if bound_form_note.is_valid() and request.user.has_perm('notes.add_note'):
            bound_form_note.save()
            note_last = Note.objects.first()
            if note_last.title == 'UWAGA' or note_last.title == 'ZGODA' or note_last.title == 'ZADANIE':
                note_last.read = False
            note_last.gadget_id = gadget_id
            note_last.author = user_id
            note_last.save()
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='login')
def add_gadget_to_worker(request, pk):
    user = request.user
    gadget = Gadget.objects.get(id=pk)
    if gadget.in_serwis:
        if Workers.objects.filter(gadget__id=pk).exists():
            s = Workers.objects.get(gadget__id=pk)
            Note.objects.create(
                author=User.objects.get(username='TPL'),
                title='ZMIANA TECHNIKA',
                content=f'{user} wziął do naprawy {gadget} od {s.worker}',
                gadget=gadget,
            )
            s.updated_at = timezone.now()
            s.worker = user
            s.in_work = True
            gadget.status = 'DIAGNOSTYKA'
            s.save()
            gadget.save()

        else:
            Workers.objects.create(worker=user, gadget=gadget)
            gadget.status = 'DIAGNOSTYKA'
            gadget.save()
            Note.objects.create(
                author=User.objects.get(username='TPL'),
                title='WZIĘTY DO NAPRAWY',
                content=f'{user} wziął do naprawy {gadget}',
                gadget=gadget,
            )
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def delete_gadget_to_worker(request, pk):
    worker = Workers.objects.filter(gadget__id=pk)
    worker.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def odstawic_gadget(request, pk):
    user = request.user
    workers_obj = Workers.objects.get(id=pk)
    gadget_id = workers_obj.gadget.id
    gadget = Gadget.objects.get(id=gadget_id)
    workers_name = workers_obj.worker
    workers_gad = workers_obj.gadget
    workers_obj.in_work = False
    workers_obj.save()

    Note.objects.create(
        author=User.objects.get(username='TPL'),
        title='NAPRAWA ZAKOŃCZONA',
        content=f'Technik {user} zakończył naprawę urządzenia',
        gadget=gadget,
    )

    if workers_obj.gadget.status == 'REZYGNACJA':
        KartkaRezygnacja.objects.create(worker=workers_name, gadget=workers_gad)
        return redirect(request.META.get('HTTP_REFERER'))
    if workers_obj.gadget.type_service == 'PŁATNE':
        KartkaPlatne.objects.create(worker=workers_name, gadget=workers_gad)
        gadget.status = 'GOTOWY'
        gadget.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if workers_obj.gadget.type_service == 'GWARANCJA':
        KartkaGwarancja.objects.create(worker=workers_name, gadget=workers_gad)
        gadget.status = 'GOTOWY'
        gadget.save()
        return redirect(request.META.get('HTTP_REFERER'))
    if workers_obj.gadget.type_service == 'REKLAMACJA':
        KartkaReklamacja.objects.create(worker=workers_name, gadget=workers_gad)
        gadget.status = 'GOTOWY'
        gadget.save()

        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def gadget_location_change(request, pk, location_id):
    gadget = Gadget.objects.get(pk=pk)
    user = request.user
    location = gadget.location
    if not location == location_id:
        Note.objects.create(
            author=User.objects.get(username='TPL'),
            title='ZMIANA LOKALIZACJI URZĄDZENIA',
            content=f'{user} przeniósł urządzenie z {location} do {location_id}',
            gadget=gadget,
        )
    gadget.location = location_id
    gadget.save()
    return redirect(request.META.get('HTTP_REFERER'))
