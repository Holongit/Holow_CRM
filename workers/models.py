from django.contrib.auth.models import User
from django.db import models
from gadgets.models import Gadget
from django.utils import timezone


class Workers(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    gadget = models.OneToOneField(Gadget, on_delete=models.CASCADE, null=True)
    added_at = models.DateTimeField(default=timezone.now, db_index=True)
    time_in = models.DurationField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=64, null=True, blank=True)
    in_work = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        ordering = ('-added_at',)

    def __str__(self):
        return self.gadget


class KartkaPlatne(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget


class KartkaGwarancja(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget


class KartkaRezygnacja(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget


class KartkaReklamacja(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget
