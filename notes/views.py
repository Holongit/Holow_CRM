from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from gadgets.models import Gadget
from notes.form import NoteForm
from notes.models import Note


@method_decorator(login_required(login_url='login'), name='dispatch')
class NoteAdd(View):
    def get(self, request, **kwargs):
        gadget = Gadget.objects.get(id=kwargs['pk'])
        notes = gadget.note_set.all()
        form = NoteForm(initial={'title': 'none'})

        return render(request, 'notes/add_note.html', context={'gadget': gadget, 'form': form, 'notes': notes})

    def post(self, request, **kwargs):
        bound_form_note = NoteForm(request.POST)
        gadget_id = Gadget.objects.get(id=kwargs['pk'])
        user_id = request.user

        if bound_form_note.is_valid() and request.user.has_perm('notes.add_note'):
            bound_form_note.save()
            note_last = Note.objects.first()
            if note_last.title == 'UWAGA' or note_last.title == 'ZGODA' or note_last.title == 'ZADANIE':
                note_last.read = False
            if note_last.title == 'DIAGNOSTYKA':
                gadget_id.status = 'WYCENA'
                gadget_id.save()
            if note_last.title == 'WYCENA':
                gadget_id.status = 'CZEKA NA ZGODĘ'
                gadget_id.save()
            if note_last.title == 'ZGODA':
                gadget_id.status = 'NAPRAWIENIE'
                gadget_id.save()
            if note_last.title == 'CZĘŚCI':
                gadget_id.status = 'CZEKA NA CZĘŚCI'
                gadget_id.save()
            note_last.gadget_id = gadget_id
            note_last.author = user_id
            note_last.save()
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def red_note(request, pk):
    note = Note.objects.get(id=pk)
    note.read = True
    note.save()
    return redirect(request.META.get('HTTP_REFERER'))
