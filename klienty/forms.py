from django import forms

from klienty.models import Klient




class KlientForm(forms.Form):

    CHOICES = (
        ('OSOBA PRYWATNA', 'OSOBA PRYWATNA'),
        ('FIRMA', 'FIRMA'),
        ('PRACOWNIK SERWISU', 'PRACOWNIK SERWISU')
    )

    name_klient = forms.CharField(max_length=64)
    telefon_klient = forms.RegexField(max_length=32, min_length=9, regex=r'^[0-9-]*$')
    opis_klient = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}), required=False)
    email_klient = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control"}), required=False)
    types_klient = forms.ChoiceField(choices=CHOICES)

    name_klient.widget.attrs.update({'class': 'form-control'})
    telefon_klient.widget.attrs.update({'class': 'form-control'})
    types_klient.widget.attrs.update({'class': 'form-control'})


    def save(self):
        new_klient = Klient.objects.create(
            name_klient=self.cleaned_data['name_klient'],
            telefon_klient=self.cleaned_data['telefon_klient'],
            opis_klient=self.cleaned_data['opis_klient'],
            email_klient=self.cleaned_data['email_klient'],
            types_klient=self.cleaned_data['types_klient'],
        )
        return new_klient
