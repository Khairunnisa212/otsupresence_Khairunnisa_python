from django.urls import path
from . import api_views

urlpatterns = [
    path('attendance/', api_views.AttendanceListAPI.as_view(), name='api_attendance_list'),
    path('attendance/<int:pk>/', api_views.AttendanceDetailAPI.as_view(), name='api_attendance_detail'),
    path('export/attendance/excel/', api_views.export_att_excel_api, name='api_export_att_excel'),
    path('export/attendance/csv/', api_views.export_att_csv_api, name='api_export_att_csv'),
    path('export/attendance/pdf/', api_views.export_att_pdf_api, name='api_export_att_pdf'),
]
