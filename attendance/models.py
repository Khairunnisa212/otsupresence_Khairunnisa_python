from django.db import models
from employees.models import Employee
from datetime import time


class Attendance(models.Model):
    STATUS_HADIR = 'hadir'
    STATUS_TERLAMBAT = 'terlambat'
    STATUS_CHOICES = [
        (STATUS_HADIR, 'Hadir'),
        (STATUS_TERLAMBAT, 'Terlambat'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    tanggal = models.DateField()
    jam_masuk = models.TimeField(null=True, blank=True)
    jam_keluar = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_HADIR)
    # Lokasi masuk
    lokasi_masuk = models.CharField(max_length=255, blank=True)
    latitude_masuk = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude_masuk = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    # Lokasi keluar
    lokasi_keluar = models.CharField(max_length=255, blank=True)
    latitude_keluar = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude_keluar = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    # Foto
    foto_masuk = models.ImageField(upload_to='attendance_photos/masuk/', null=True, blank=True)
    foto_keluar = models.ImageField(upload_to='attendance_photos/keluar/', null=True, blank=True)
    keterangan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['employee', 'tanggal']
        ordering = ['-tanggal', '-jam_masuk']
        verbose_name = 'Absensi'
        verbose_name_plural = 'Absensi'

    def save(self, *args, **kwargs):
        if self.jam_masuk:
            batas_terlambat = time(8, 30)
            self.status = self.STATUS_TERLAMBAT if self.jam_masuk > batas_terlambat else self.STATUS_HADIR
        super().save(*args, **kwargs)

    @property
    def durasi_kerja(self):
        if self.jam_masuk and self.jam_keluar:
            from datetime import datetime, date as date_cls
            masuk = datetime.combine(date_cls.today(), self.jam_masuk)
            keluar = datetime.combine(date_cls.today(), self.jam_keluar)
            if keluar <= masuk:
                return '-'
            durasi = keluar - masuk
            hours = int(durasi.total_seconds() // 3600)
            minutes = int((durasi.total_seconds() % 3600) // 60)
            return f"{hours}j {minutes}m"
        return '-'

    def __str__(self):
        return f"{self.employee.nama} - {self.tanggal} ({self.get_status_display()})"
