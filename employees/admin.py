from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['nomor_karyawan', 'nama', 'jabatan', 'departemen', 'status_aktif', 'tanggal_masuk']
    list_filter = ['status_aktif', 'departemen']
    search_fields = ['nama', 'email', 'nomor_karyawan']
