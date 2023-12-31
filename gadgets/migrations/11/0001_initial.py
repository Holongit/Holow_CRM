# Generated by Django 4.2.8 on 2023-12-26 14:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gadget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master_gadget', models.CharField(db_index=True, default='TPL', max_length=64)),
                ('telefon_master_gadget', models.CharField(db_index=True, max_length=32)),
                ('serial_gadget', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('model_gadget', models.CharField(db_index=True, max_length=32)),
                ('brand_gadget', models.CharField(db_index=True, max_length=32)),
                ('type_gadget', models.CharField(db_index=True, max_length=32)),
                ('password_gadget', models.CharField(blank=True, max_length=64, null=True)),
                ('opis_problem', models.TextField(blank=True, null=True)),
                ('zestaw', models.CharField(blank=True, max_length=64, null=True)),
                ('pilne', models.CharField(blank=True, db_index=True, default='NO', max_length=32, null=True)),
                ('status', models.CharField(blank=True, db_index=True, default='NEW', max_length=32, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Klient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_klient', models.CharField(db_index=True, max_length=64)),
                ('telefon_klient', models.CharField(db_index=True, max_length=32)),
                ('email_klient', models.CharField(blank=True, max_length=64, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
