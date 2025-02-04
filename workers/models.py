from django.contrib.auth.models import User
from django.db import models
from gadgets.models import Gadget
from django.utils import timezone


TODAY = timezone.now()


class Workers(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    gadget = models.OneToOneField(Gadget, on_delete=models.CASCADE, null=True)
    added_at = models.DateTimeField(default=timezone.now, db_index=True)
    time_in = models.DurationField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=64, null=True, blank=True)
    in_work = models.BooleanField(default=True, null=True, blank=True)

    def added_at_format(self):
        return self.added_at.strftime("%d.%m.%y %H:%M")

    def time_in_worker(self):
        time = timezone.now() - self.updated_at
        return time.days

    def time_in_work(self):
        time = timezone.now() - self.added_at
        return time.days

    class Meta:
        ordering = ('-added_at',)

    def __str__(self):
        return self.gadget


class KartkaPlatne(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    def created_at_format(self):
        return self.created_at.strftime("%d.%m.%y %H:%M")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget

    def get_platne_day_worker_count(self):
        qnt_all = KartkaPlatne.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__day=TODAY.day).count()

    def get_platne_month_worker_count(self):
        qnt_all = KartkaPlatne.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__month=TODAY.month).count()

    def get_platne_year_worker_count(self):
        qnt_all = KartkaPlatne.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__year=TODAY.year).count()


class KartkaGwarancja(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    def created_at_format(self):
        return self.created_at.strftime("%d.%m.%y %H:%M")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget

    def get_gwarancja_day_worker_count(self):
        qnt_all = KartkaGwarancja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__day=TODAY.day).count()

    def get_gwarancja_month_worker_count(self):
        qnt_all = KartkaGwarancja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__month=TODAY.month).count()

    def get_gwarancja_year_worker_count(self):
        qnt_all = KartkaGwarancja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__year=TODAY.year).count()

class KartkaRezygnacja(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    def created_at_format(self):
        return self.created_at.strftime("%d.%m.%y %H:%M")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget

    def get_rezygnacja_day_worker_count(self):
        qnt_all = KartkaRezygnacja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__day=TODAY.day).count()

    def get_rezygnacja_month_worker_count(self):
        qnt_all = KartkaRezygnacja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__month=TODAY.month).count()

    def get_rezygnacja_year_worker_count(self):
        qnt_all = KartkaRezygnacja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__year=TODAY.year).count()


class KartkaReklamacja(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qnt = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, null=True)

    def created_at_format(self):
        return self.created_at.strftime("%d.%m.%y %H:%M")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.gadget

    def get_reklamacja_day_worker_count(self):
        qnt_all = KartkaReklamacja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__day=TODAY.day).count()

    def get_reklamacja_month_worker_count(self):
        qnt_all = KartkaReklamacja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__month=TODAY.month).count()

    def get_reklamacja_year_worker_count(self):
        qnt_all = KartkaReklamacja.objects.filter(worker=self.worker)
        return qnt_all.filter(created_at__year=TODAY.year).count()
