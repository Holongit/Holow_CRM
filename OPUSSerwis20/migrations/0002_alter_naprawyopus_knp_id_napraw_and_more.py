# Generated by Django 4.2.8 on 2024-01-27 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('klienty', '0004_alter_klient_options'),
        ('OPUSSerwis20', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naprawyopus',
            name='KNP_ID_NAPRAW',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OPUSSerwis20.pracownikiopus'),
        ),
        migrations.AlterField(
            model_name='naprawyopus',
            name='KNP_NR_WLASCICIELA',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='klienty.klient'),
        ),
        migrations.AlterField(
            model_name='naprawyopus',
            name='KNP_PRD_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='OPUSSerwis20.productyopus'),
        ),
    ]