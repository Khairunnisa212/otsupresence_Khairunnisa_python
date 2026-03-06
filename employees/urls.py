from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('karyawan/', views.employee_list, name='employee_list'),
    path('karyawan/tambah/', views.employee_create, name='employee_create'),
    # Export routes MUST come before <int:pk> to avoid 'export' being parsed as pk
    path('karyawan/export/excel/', views.export_employees_excel, name='export_employees_excel'),
    path('karyawan/export/csv/', views.export_employees_csv, name='export_employees_csv'),
    path('karyawan/export/pdf/', views.export_employees_pdf, name='export_employees_pdf'),
    path('karyawan/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('karyawan/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('karyawan/<int:pk>/hapus/', views.employee_delete, name='employee_delete'),
]
