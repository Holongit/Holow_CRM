from django.contrib.auth.models import User
from django.db import models


class ServisLocationList(models.Model):
    servis_name = models.CharField(max_length=32, null=True, blank=True)
    servis_location = models.CharField(max_length=32)
    servis_adress = models.CharField(max_length=512, null=True, blank=True)
    servis_telephone = models.CharField(max_length=32, null=True, blank=True)
    servis_email = models.CharField(max_length=32, null=True, blank=True)
    servis_opis = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.servis_location
