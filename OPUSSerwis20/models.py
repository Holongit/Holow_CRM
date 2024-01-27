from django.db import models
from klienty.models import Klient


class ProductyOPUS(models.Model):
    PRD_ID = models.PositiveIntegerField(primary_key=True)
    PRD_NAZWA = models.CharField(max_length=32)

    def __str__(self):
        return self.PRD_NAZWA


class PracownikiOpus(models.Model):
    PRC_ID = models.PositiveIntegerField(primary_key=True)
    PRC_IMIE = models.CharField(max_length=32)
    PRC_NAZWISKO = models.CharField(max_length=32, blank=True, null=True)
    PRC_LOGIN = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.PRC_LOGIN


class NaprawyOpus(models.Model):
    KNP_NR_SER_KOL = models.CharField(max_length=12)
    KNP_NR_ROK = models.CharField(max_length=12)
    KNP_NR_SERYJNY = models.CharField(max_length=64, blank=True, null=True)
    KNP_PRD_ID = models.ForeignKey(ProductyOPUS, on_delete=models.CASCADE, blank=True, null=True)
    KNP_POCZATEK_NAPRAWY = models.CharField(max_length=64, blank=True, null=True)
    KNP_PR_DATA_KONCANAPR = models.CharField(max_length=64, blank=True, null=True)
    KNP_NR_WLASCICIELA = models.ForeignKey(Klient, on_delete=models.CASCADE, blank=True, null=True)
    KNP_OPIS_USTERKI = models.CharField(max_length=512, blank=True, null=True)
    KNP_UWAGI = models.CharField(max_length=512, blank=True, null=True)
    KNP_WYKONANE_NAPRAWY = models.CharField(max_length=512, blank=True, null=True)
    KNP_OPIS_WYPOSAZENIA = models.CharField(max_length=512, blank=True, null=True)
    KNP_ID_NAPRAW = models.ForeignKey(PracownikiOpus, on_delete=models.CASCADE, blank=True, null=True)
    KNP_POLEDODATKOWE1 = models.CharField(max_length=256, blank=True, null=True)
    KNP_POLEDODATKOWE2 = models.CharField(max_length=256, blank=True, null=True)
    KNP_POLEDODATKOWE3 = models.CharField(max_length=256, blank=True, null=True)
    KNP_POLEDODATKOWE4 = models.CharField(max_length=256, blank=True, null=True)
    KNP_POLEDODATKOWE5 = models.CharField(max_length=256, blank=True, null=True)
    KNP_POLEDODATKOWE6 = models.CharField(max_length=256, blank=True, null=True)
    KNP_POLEDODATKOWE7 = models.CharField(max_length=256, blank=True, null=True)
    KNP_POLEDODATKOWE8 = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.KNP_NR_SERYJNY

    class Meta:
        ordering = ('-id',)

















