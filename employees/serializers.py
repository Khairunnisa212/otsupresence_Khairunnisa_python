from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    status_aktif_display = serializers.CharField(source='get_status_aktif_display', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['nomor_karyawan', 'created_at', 'updated_at']
