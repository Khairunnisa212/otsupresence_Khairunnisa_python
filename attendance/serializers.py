from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_nama = serializers.CharField(source='employee.nama', read_only=True)
    employee_nomor = serializers.CharField(source='employee.nomor_karyawan', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    durasi = serializers.CharField(source='durasi_kerja', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
