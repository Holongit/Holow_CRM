# Generated by Django 4.2.8 on 2024-01-01 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gadgets', '0005_alter_gadget_opis_naprawy'),
    ]

    operations = [
        migrations.AddField(
            model_name='gadget',
            name='type_service',
            field=models.TextField(default='Płatna'),
        ),
        migrations.AlterField(
            model_name='gadget',
            name='opis_naprawy',
            field=models.TextField(blank=True, null=True),
        ),
    ]
