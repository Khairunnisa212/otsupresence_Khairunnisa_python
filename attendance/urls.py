from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('laporan/', views.monthly_report, name='monthly_report'),
    path('export/excel/', views.export_attendance_excel, name='export_attendance_excel'),
    path('export/csv/', views.export_attendance_csv, name='export_attendance_csv'),
    path('export/pdf/', views.export_attendance_pdf, name='export_attendance_pdf'),
]
