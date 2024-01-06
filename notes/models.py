from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from gadgets.models import Gadget
from klienty.models import Klient

class Note(models.Model):
    author = models.CharField(max_length=32, default='Andrej Khairov')
    title = models.CharField(max_length=32, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    destination = models.CharField(max_length=32, default='MANAGER')
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-created_at',)
