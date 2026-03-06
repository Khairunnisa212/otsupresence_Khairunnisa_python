from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'tanggal', 'jam_masuk', 'jam_keluar', 'status']
    list_filter = ['status', 'tanggal']
    search_fields = ['employee__nama', 'employee__nomor_karyawan']
    date_hierarchy = 'tanggal'
