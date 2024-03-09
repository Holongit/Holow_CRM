from django import forms
from django.core.validators import RegexValidator
from django.forms import RadioSelect

from notes.models import Note
from gadgets.models import Gadget

class NoteForm(forms.Form):
    CHOICES = (
        ('DIAGNOSTYKA', 'DIAGNOSTYKA'),
        ('CZĘŚCI', 'CZĘŚCI'),
        ('UWAGA', 'UWAGA'),
        ('ZGODA', 'ZGODA'),
        ('ZADANIE', 'ZADANIE'),
        ('WYCENA', 'WYCENA'),
        ('none', '')
    )
    content = forms.CharField()
    title = forms.ChoiceField(choices=CHOICES)

    content.widget.attrs.update({'class': 'form-control', 'placeholder': 'notatka'})
    title.widget.attrs.update({'class': 'form-control'})

    def save(self):
        new_note = Note.objects.create(
            title=self.cleaned_data['title'],
            content=self.cleaned_data['content'],
        )
        return new_note

