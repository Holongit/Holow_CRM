# Generated by Django 4.2.8 on 2024-03-24 11:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gadgets', '0011_gadget_managed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='gadget',
            name='alarm_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
