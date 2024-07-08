from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class Users(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Peminjam', 'Peminjam')
    ]    
    fullname = models.CharField(max_length=40)
    email = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    password = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    # def __unicode__(self):
        # return self.fullname 
    
class Gedung(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi_gedung = models.TextField(null=True)
    alamat = models.TextField()
    image = models.ImageField(upload_to='uploads/', null=True) 

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
    id_peminjam = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

