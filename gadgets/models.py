from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.duration import duration_string

from klienty.models import Klient


class Gadget(models.Model):
    serial_gadget = models.CharField(max_length=32, null=True, blank=True, db_index=True)
    model_gadget = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    brand_gadget = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    type_gadget = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    password_gadget = models.CharField(max_length=64, null=True, blank=True)
    opis_problem = models.TextField(null=True, blank=True)
    zestaw = models.CharField(max_length=64, null=True, blank=True)
    pilne = models.CharField(max_length=32, default='NIE', null=True, blank=True, db_index=True)
    status = models.CharField(max_length=32, default='NOWY', null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    managed_at = models.DateTimeField(default=timezone.now)
    alarm_at = models.DateTimeField(default=timezone.now)
    alarm_on = models.BooleanField(default=False, blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    klient = models.ForeignKey(Klient, on_delete=models.PROTECT, null=True)
    location = models.CharField(max_length=32, default='STOKŁOSY', db_index=True, blank=True, null=True)
    paid = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    in_serwis = models.BooleanField(default=True, db_index=True, blank=True, null=True)
    time_in_serwis = models.DurationField(null=True, blank=True)
    opis_naprawy = models.CharField(max_length=512, null=True, blank=True)
    usterki_zewn = models.CharField(max_length=512, null=True, blank=True)
    type_service = models.CharField(max_length=32, default='PŁATNE', blank=True, null=True)
    technik_ost = models.CharField(max_length=32, null=True, blank=True)

    def created_at_format(self):
        return self.created_at.strftime("%d.%m.%y %H:%M")

    def updated_at_format(self):
        return self.updated_at.strftime("%d.%m.%y %H:%M")

    def time_in_serwis_get(self):
        time = timezone.now() - self.updated_at
        return time.days

    def time_in_status_get(self):
        time = timezone.now() - self.managed_at
        return time.days

    def time_alarm_get(self):
        if self.alarm_on:
            time = self.alarm_at - timezone.now()
            return duration_string(time)[:-7]

    def alarm_gadget(self):
        if timezone.now() > self.alarm_at and self.alarm_on:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('edit_gadget', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.model_gadget

    def unread_note(self):
        if self.note_set.filter(read=False).exists():
            return True


class SetingsCRM(models.Model):
    filter_gadget = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    filter_manager = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    filter_manager_gotowy = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_zaliczka = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_nowy = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_rezygnacja = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_czeka_na_zgode = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_wycena = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_diagnostyka = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_czeka_na_części = models.BooleanField(default=True, blank=True, null=True)
    filter_manager_naprawienie = models.BooleanField(default=True, blank=True, null=True)
    filter_klient = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    filter_dashboar = models.CharField(max_length=16, default='STOKŁOSY', null=True, blank=True)
    filter_work = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.filter_gadget
