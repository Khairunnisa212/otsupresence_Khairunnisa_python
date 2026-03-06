from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceListAPI(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'tanggal']
    search_fields = ['employee__nama', 'employee__nomor_karyawan']
    ordering_fields = ['tanggal', 'jam_masuk', 'status']
    ordering = ['-tanggal']

    def get_queryset(self):
        if self.request.user.is_admin_role:
            return Attendance.objects.select_related('employee').all()
        try:
            return Attendance.objects.filter(employee=self.request.user.employee_profile)
        except Exception:
            return Attendance.objects.none()


class AttendanceDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_att_excel_api(request):
    from attendance.views import export_attendance_excel
    return export_attendance_excel(request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_att_csv_api(request):
    from attendance.views import export_attendance_csv
    return export_attendance_csv(request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_att_pdf_api(request):
    from attendance.views import export_attendance_pdf
    return export_attendance_pdf(request)
