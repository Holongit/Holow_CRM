# Generated by Django 4.2.8 on 2024-01-27 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('klienty', '0004_alter_klient_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PracownikiOpus',
            fields=[
                ('PRC_ID', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('PRC_IMIE', models.CharField(max_length=32)),
                ('PRC_NAZWISKO', models.CharField(blank=True, max_length=32, null=True)),
                ('PRC_LOGIN', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductyOPUS',
            fields=[
                ('PRD_ID', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('PRD_NAZWA', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='NaprawyOpus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('KNP_NR_SER_KOL', models.CharField(max_length=12)),
                ('KNP_NR_ROK', models.CharField(max_length=12)),
                ('KNP_NR_SERYJNY', models.CharField(blank=True, max_length=64, null=True)),
                ('KNP_PRD_ID', models.CharField(blank=True, max_length=64, null=True)),
                ('KNP_POCZATEK_NAPRAWY', models.CharField(blank=True, max_length=64, null=True)),
                ('KNP_PR_DATA_KONCANAPR', models.CharField(blank=True, max_length=64, null=True)),
                ('KNP_OPIS_USTERKI', models.CharField(blank=True, max_length=512, null=True)),
                ('KNP_UWAGI', models.CharField(blank=True, max_length=512, null=True)),
                ('KNP_WYKONANE_NAPRAWY', models.CharField(blank=True, max_length=512, null=True)),
                ('KNP_OPIS_WYPOSAZENIA', models.CharField(blank=True, max_length=512, null=True)),
                ('KNP_ID_NAPRAW', models.CharField(blank=True, max_length=64, null=True)),
                ('KNP_POLEDODATKOWE1', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_POLEDODATKOWE2', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_POLEDODATKOWE3', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_POLEDODATKOWE4', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_POLEDODATKOWE5', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_POLEDODATKOWE6', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_POLEDODATKOWE7', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_POLEDODATKOWE8', models.CharField(blank=True, max_length=256, null=True)),
                ('KNP_NR_WLASCICIELA', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='klienty.klient')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
