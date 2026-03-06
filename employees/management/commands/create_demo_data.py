from django.core.management.base import BaseCommand
from datetime import date, timedelta, time
import random


class Command(BaseCommand):
    help = 'Buat data demo OtsuPresence (admin + karyawan + riwayat absensi)'

    def handle(self, *args, **kwargs):
        from accounts.models import User
        from employees.models import Employee
        from attendance.models import Attendance

        self.stdout.write(self.style.MIGRATE_HEADING('\n=== OtsuPresence — Membuat Data Demo ===\n'))

        # ─── ADMIN ───
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@otsuka.co.id',
                password='admin123',
                first_name='Admin',
                last_name='Sistem',
                role=User.ROLE_ADMIN,
            )
            self.stdout.write(self.style.SUCCESS('  [+] Admin    : admin / admin123'))
        else:
            self.stdout.write('  [~] Admin sudah ada, dilewati')

        # ─── DATA KARYAWAN ───
        karyawan_data = [
            {'nama': 'Budi Santoso',    'email': 'budi@otsuka.co.id',   'jabatan': 'Software Engineer',     'dept': 'Engineering',  'username': 'budi'},
            {'nama': 'Siti Rahayu',     'email': 'siti@otsuka.co.id',   'jabatan': 'UI/UX Designer',        'dept': 'Design',       'username': 'siti'},
            {'nama': 'Ahmad Fauzi',     'email': 'ahmad@otsuka.co.id',  'jabatan': 'Project Manager',       'dept': 'Management',   'username': 'ahmad'},
            {'nama': 'Dewi Lestari',    'email': 'dewi@otsuka.co.id',   'jabatan': 'Marketing Specialist',  'dept': 'Marketing',    'username': 'dewi'},
            {'nama': 'Rizky Pratama',   'email': 'rizky@otsuka.co.id',  'jabatan': 'Backend Developer',     'dept': 'Engineering',  'username': 'rizky'},
            {'nama': 'Nur Aisyah',      'email': 'nur@otsuka.co.id',    'jabatan': 'HR Specialist',         'dept': 'HR',           'username': 'nur'},
            {'nama': 'Andi Wijaya',     'email': 'andi@otsuka.co.id',   'jabatan': 'Frontend Developer',    'dept': 'Engineering',  'username': 'andi'},
            {'nama': 'Maya Sari',       'email': 'maya@otsuka.co.id',   'jabatan': 'Accounting Staff',      'dept': 'Finance',      'username': 'maya'},
        ]

        self.stdout.write('')
        created_employees = []
        for i, d in enumerate(karyawan_data):
            if Employee.objects.filter(email=d['email']).exists():
                self.stdout.write(f"  [~] {d['nama']} sudah ada, dilewati")
                created_employees.append(Employee.objects.get(email=d['email']))
                continue

            # Buat employee
            emp = Employee.objects.create(
                nama=d['nama'],
                email=d['email'],
                jabatan=d['jabatan'],
                departemen=d['dept'],
                tanggal_masuk=date(2023, random.randint(1, 12), random.randint(1, 28)),
                status_aktif='aktif',
                telepon=f'08{random.randint(100000000, 999999999)}',
            )

            # Buat user login
            if not User.objects.filter(username=d['username']).exists():
                user = User.objects.create_user(
                    username=d['username'],
                    email=d['email'],
                    password='karyawan123',
                    first_name=d['nama'].split()[0],
                    last_name=' '.join(d['nama'].split()[1:]),
                    role=User.ROLE_EMPLOYEE,
                )
                emp.user = user
                emp.save()

            created_employees.append(emp)
            self.stdout.write(self.style.SUCCESS(
                f"  [+] Karyawan  : {d['username']} / karyawan123  ({d['nama']} — {d['dept']})"
            ))

        # ─── DATA ABSENSI (30 hari terakhir) ───
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('  Membuat riwayat absensi 30 hari...'))

        today = date.today()
        lokasi_list = [
            'Kantor Pusat Jakarta',
            'Kantor Pusat Jakarta',
            'Kantor Pusat Jakarta',
            'CV. Indosistem',
            'Client Site — Sudirman',
        ]
        total_created = 0

        for emp in Employee.objects.all():
            for days_ago in range(30, 0, -1):
                att_date = today - timedelta(days=days_ago)

                # Skip sabtu minggu
                if att_date.weekday() >= 5:
                    continue

                # Skip kalau sudah ada
                if Attendance.objects.filter(employee=emp, tanggal=att_date).exists():
                    continue

                # 88% hadir
                if random.random() > 0.88:
                    continue

                # Jam masuk: 07:30 - 09:00 (20% terlambat > 08:30)
                if random.random() < 0.20:
                    jam_masuk = time(random.randint(8, 9), random.randint(31, 59))
                else:
                    jam_masuk = time(random.randint(7, 8), random.randint(0, 29))

                # Jam keluar: 16:00 - 18:30
                jam_keluar = time(random.randint(16, 18), random.randint(0, 59))

                Attendance.objects.create(
                    employee=emp,
                    tanggal=att_date,
                    jam_masuk=jam_masuk,
                    jam_keluar=jam_keluar,
                    lokasi_masuk=random.choice(lokasi_list),
                    lokasi_keluar='Kantor Pusat Jakarta',
                    latitude_masuk=-6.2088 + random.uniform(-0.001, 0.001),
                    longitude_masuk=106.8456 + random.uniform(-0.001, 0.001),
                )
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f'  [+] {total_created} record absensi dibuat'))

        # ─── SUMMARY ───
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('=== Selesai! ==='))
        self.stdout.write('')
        self.stdout.write('  Akses: http://localhost:8000')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('  Login Admin    : admin / admin123'))
        self.stdout.write(self.style.SUCCESS('  Login Karyawan : budi / karyawan123'))
        self.stdout.write(self.style.SUCCESS('  Login Karyawan : siti / karyawan123'))
        self.stdout.write(self.style.SUCCESS('  (dan seterusnya: ahmad, dewi, rizky, nur, andi, maya)'))
        self.stdout.write('')
