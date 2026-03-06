from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from .models import Employee
from .serializers import EmployeeSerializer
import csv
import io
from datetime import date


class EmployeeListAPI(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status_aktif', 'departemen']
    search_fields = ['nama', 'email', 'jabatan', 'nomor_karyawan']
    ordering_fields = ['nama', 'tanggal_masuk', 'jabatan', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_admin_role:
            return Employee.objects.all()
        try:
            return Employee.objects.filter(id=self.request.user.employee_profile.id)
        except Exception:
            return Employee.objects.none()


class EmployeeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_employees_excel_api(request):
    from employees.views import export_employees_excel
    return export_employees_excel(request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_employees_csv_api(request):
    from employees.views import export_employees_csv
    return export_employees_csv(request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_employees_pdf_api(request):
    from employees.views import export_employees_pdf
    return export_employees_pdf(request)
