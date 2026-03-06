from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from employees.models import Employee
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Buat akun demo untuk Railway deployment'

    def handle(self, *args, **kwargs):
        # Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@demo.com',
                password='password123',
                first_name='Admin',
                last_name='Demo',
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin created: admin@demo.com / password123'))
        else:
            self.stdout.write('  Admin already exists.')

        # Karyawan demo
        if not User.objects.filter(username='karyawan').exists():
            user = User.objects.create_user(
                username='karyawan',
                email='user@demo.com',
                password='password123',
                first_name='Budi',
                last_name='Santoso',
                role='employee',
            )
            if not Employee.objects.filter(email='user@demo.com').exists():
                Employee.objects.create(
                    user=user,
                    nama='Budi Santoso',
                    email='user@demo.com',
                    jabatan='Staff IT',
                    departemen='Teknologi',
                    tanggal_masuk=date(2023, 1, 15),
                    status_aktif='aktif',
                )
            self.stdout.write(self.style.SUCCESS('✓ Karyawan created: user@demo.com / password123'))
        else:
            self.stdout.write('  Karyawan already exists.')

        self.stdout.write(self.style.SUCCESS('\n✅ Demo users ready!'))
        self.stdout.write('   Admin    → admin@demo.com / password123')
        self.stdout.write('   Karyawan → user@demo.com  / password123')
