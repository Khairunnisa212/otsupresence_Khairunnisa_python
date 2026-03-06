from django.db import models
from accounts.models import User


class Employee(models.Model):
    STATUS_AKTIF = 'aktif'
    STATUS_NONAKTIF = 'nonaktif'
    STATUS_CHOICES = [
        (STATUS_AKTIF, 'Aktif'),
        (STATUS_NONAKTIF, 'Nonaktif'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    nama = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    jabatan = models.CharField(max_length=200)
    departemen = models.CharField(max_length=200, default='Umum')
    tanggal_masuk = models.DateField()
    status_aktif = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AKTIF)
    nomor_karyawan = models.CharField(max_length=20, unique=True, blank=True)
    foto = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    telepon = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Karyawan'
        verbose_name_plural = 'Karyawan'

    def save(self, *args, **kwargs):
        if not self.nomor_karyawan:
            from django.db import transaction
            with transaction.atomic():
                last = Employee.objects.select_for_update().order_by('-id').first()
                last_id = (last.id + 1) if last else 1
                self.nomor_karyawan = f'KRY-{last_id:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama} ({self.nomor_karyawan})"

    @property
    def is_active(self):
        return self.status_aktif == self.STATUS_AKTIF
