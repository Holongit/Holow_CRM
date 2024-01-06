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

