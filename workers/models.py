from django.contrib.auth.models import User
from django.db import models
from gadgets.models import Gadget
from django.utils import timezone


class Workers(models.Model):
    worker = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    gadget = models.OneToOneField(Gadget, on_delete=models.DO_NOTHING, null=True)
    added_at = models.DateTimeField(default=timezone.now, db_index=True)
    time_in = models.DurationField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=16, null=True, blank=True, default='W_PRACE')



    class Meta:
        ordering = ('-added_at',)

    def __str__(self):
        return self.gadget

