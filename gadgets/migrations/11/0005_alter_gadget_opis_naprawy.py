# Generated by Django 4.2.8 on 2024-01-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gadgets', '0004_gadget_opis_naprawy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gadget',
            name='opis_naprawy',
            field=models.TextField(default='Płatna'),
        ),
    ]
