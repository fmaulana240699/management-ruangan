# Generated by Django 5.0.3 on 2024-03-28 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gedung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('alamat', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReservasiGedung',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_peminjaman', models.DateTimeField()),
                ('end_peminjaman', models.DateTimeField()),
                ('deskripsi_kegiatan', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('id_gedung', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.gedung')),
            ],
        ),
    ]
