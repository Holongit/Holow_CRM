# Generated by Django 4.2.8 on 2024-01-20 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gadgets', '0005_alter_gadget_opis_naprawy_alter_gadget_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gadget',
            name='master_gadget',
        ),
        migrations.RemoveField(
            model_name='gadget',
            name='telefon_master_gadget',
        ),
    ]