from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_EMPLOYEE = 'employee'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_EMPLOYEE, 'Karyawan'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    @property
    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_employee_role(self):
        return self.role == self.ROLE_EMPLOYEE

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
