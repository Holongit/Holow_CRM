# Generated by Django 4.2.8 on 2024-02-03 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gadgets', '0008_gadget_technik_ost'),
        ('workers', '0003_alter_workers_gadget_alter_workers_worker'),
    ]

    operations = [
        migrations.CreateModel(
            name='KartkaRezygnacja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qnt', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('gadget', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gadgets.gadget')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='KartkaReklamacja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qnt', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('gadget', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gadgets.gadget')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='KartkaPlatne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qnt', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('gadget', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gadgets.gadget')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='KartkaGwarancja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qnt', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('gadget', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gadgets.gadget')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]