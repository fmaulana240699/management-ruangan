from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

class Gedung(models.Model):
    nama = models.CharField(max_length=100)
    alamat = models.TextField()

class ReservasiGedung(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    start_peminjaman = models.DateTimeField()
    end_peminjaman = models.DateTimeField()
    id_gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE, null=True)
    deskripsi_kegiatan = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")