from django.db import models
from django.utils import timezone


class Klient(models.Model):
    name_klient = models.CharField(max_length=64, db_index=True)
    telefon_klient = models.CharField(max_length=32, db_index=True, null=True, blank=True)
    email_klient = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    opis_klient = models.CharField(max_length=128, null=True, blank=True)
    types_klient = models.CharField(max_length=32, null=True, blank=True)
    in_serwis = models.BooleanField(default=True, null=True, blank=True)
    kasa_klient = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)

    def time_with_serwis_get(self):
        time = timezone.now() - self.created_at
        return time.days

    def created_at_format(self):
        return self.created_at.strftime("%d.%m.%y %H:%M")

    def __str__(self):
        return self.name_klient

    class Meta:
        ordering = ('-id',)
