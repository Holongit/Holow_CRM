# Generated by Django 4.2.8 on 2024-01-14 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gadgets', '0004_alter_gadget_klient'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workers', '0002_workers_status_alter_workers_added_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workers',
            name='gadget',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gadgets.gadget'),
        ),
        migrations.AlterField(
            model_name='workers',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]