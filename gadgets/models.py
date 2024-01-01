from django.db import models
from django.utils import timezone
from django.urls import reverse


class Klient(models.Model):
    name_klient = models.CharField(max_length=64, db_index=True)
    telefon_klient = models.CharField(max_length=32, db_index=True)
    email_klient = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name_klient

    class Meta:
        ordering = ('-created_at',)


class Gadget(models.Model):
    master_gadget = models.CharField(max_length=64, default='TPL', db_index=True)
    telefon_master_gadget = models.CharField(max_length=32, db_index=True)
    serial_gadget = models.CharField(max_length=32, null=True, blank=True, db_index=True)
    model_gadget = models.CharField(max_length=32, db_index=True)
    brand_gadget = models.CharField(max_length=32, db_index=True)
    type_gadget = models.CharField(max_length=32, db_index=True)
    password_gadget = models.CharField(max_length=64, null=True, blank=True)
    opis_problem = models.TextField(null=True, blank=True)
    zestaw = models.CharField(max_length=64, null=True, blank=True)
    pilne = models.CharField(max_length=32, default='NO', null=True, blank=True, db_index=True)
    status = models.CharField(max_length=32, default='NOWY', null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    location = models.CharField(max_length=32, default='STOKŁOSY', db_index=True)
    paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    in_serwis = models.BooleanField(default=True, db_index=True)
    time_in_serwis = models.DurationField(null=True, blank=True)
    opis_naprawy = models.TextField(null=True, blank=True)
    type_service = models.CharField(max_length=32, default='PŁATNE')


    def get_absolute_url(self):
        return reverse('edit_gadget', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-created_at',)


    def __str__(self):
        return self.model_gadget

class SetingsCRM(models.Model):
    filter_gadget = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    filter_klient = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    filter_dashboar = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    filter_work = models.CharField(max_length=16, default='WSZYSCY', null=True, blank=True)
    def __str__(self):
        return self.filter_gadget