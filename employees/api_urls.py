from django.urls import path
from . import api_views

urlpatterns = [
    path('employees/', api_views.EmployeeListAPI.as_view(), name='api_employee_list'),
    path('employees/<int:pk>/', api_views.EmployeeDetailAPI.as_view(), name='api_employee_detail'),
    path('export/employees/excel/', api_views.export_employees_excel_api, name='api_export_emp_excel'),
    path('export/employees/csv/', api_views.export_employees_csv_api, name='api_export_emp_csv'),
    path('export/employees/pdf/', api_views.export_employees_pdf_api, name='api_export_emp_pdf'),
]
