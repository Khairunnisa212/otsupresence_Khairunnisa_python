# OtsuPresence

**Sistem Manajemen Kehadiran Karyawan — PT Otsuka Indonesia**

Aplikasi absensi berbasis web yang dapat diakses dari smartphone. Karyawan dapat melakukan check-in dan check-out lengkap dengan foto selfie dan GPS location tracking — tanpa perlu install aplikasi apapun.

---

## Fitur Utama

- **Absensi via Smartphone** — check-in & check-out langsung dari browser HP
- **Foto Selfie** — kamera otomatis aktif saat absen, foto tersimpan ke database
- **GPS Location** — koordinat & nama lokasi otomatis terdeteksi via Nominatim
- **Status Otomatis** — sistem menentukan `hadir` atau `terlambat` (batas 08:30)
- **Dashboard Real-time** — data langsung terupdate setelah absen
- **Laporan Bulanan** — rekap kehadiran per karyawan + grafik
- **Export Data** — unduh laporan dalam format Excel, CSV, PDF
- **Multi-role** — tampilan berbeda untuk Admin dan Karyawan

---

## Tech Stack

| Layer | Teknologi |
|---|---|
| Backend | Django 5.2 |
| Database | MySQL 8.0 |
| Frontend | Tailwind CSS v3 (CDN) + Vanilla JS |
| API | Django REST Framework |
| Deploy | Docker + Docker Compose |

---

## Setup Lokal (Windows + MySQL)

### Prasyarat

Pastikan sudah terinstall:
- Python 3.10 atau lebih baru → [python.org](https://python.org)
- MySQL 8.0 → [mysql.com](https://dev.mysql.com/downloads/installer/)
- Git (opsional) → [git-scm.com](https://git-scm.com)

---

### Langkah 1 — Ekstrak & Masuk ke Folder

```bash
# Ekstrak ZIP, lalu masuk ke folder project
cd otsupresence_fixed
```

---

### Langkah 2 — Buat Virtual Environment

```bash
# Buat environment
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Mac/Linux)
source venv/bin/activate
```

---

### Langkah 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Langkah 4 — Buat Database MySQL

Buka MySQL Workbench atau Command Prompt MySQL, lalu jalankan:

```sql
CREATE DATABASE otsupresence_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

---

### Langkah 5 — Konfigurasi File `.env`

Copy file contoh lalu edit:

```bash
copy .env.example .env
```

Buka file `.env` dan isi sesuai konfigurasi lokal:

```env
# Generate secret key baru dengan perintah ini:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

SECRET_KEY=isi-dengan-secret-key-yang-digenerate
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Sesuaikan dengan MySQL kamu
DB_ENGINE=mysql
DB_NAME=otsupresence_db
DB_USER=root
DB_PASSWORD=password_mysql_kamu
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

### Langkah 6 — Jalankan Migrasi Database

```bash
python manage.py migrate
```

Perintah ini akan membuat semua tabel (`accounts_user`, `employees_employee`, `attendance_attendance`, dll) secara otomatis di database MySQL.

---

### Langkah 7 — Buat Data Demo (Opsional)

```bash
python manage.py create_demo_data
```

Perintah ini akan membuat:
- 1 akun admin + 5 karyawan demo
- Data absensi selama 30 hari terakhir

---

### Langkah 8 — Jalankan Server

```bash
python manage.py runserver
```

Buka browser dan akses: **http://127.0.0.1:8000**

---

### Akses dari Smartphone (Jaringan Lokal)

Agar smartphone bisa mengakses server di komputer yang sama jaringan Wi-Fi:

```bash
# Cari IP komputer kamu (Windows)
ipconfig

# Jalankan server dengan IP lokal
python manage.py runserver 0.0.0.0:8000
```

Kemudian buka di browser HP: `http://[IP-KOMPUTER]:8000`

Contoh: `http://192.168.1.10:8000`

> **Catatan:** Fitur kamera (foto selfie) memerlukan koneksi HTTPS di browser Chrome/Safari untuk production. Untuk testing lokal, gunakan Firefox atau aktifkan HTTPS.

---

## Setup via Docker (Alternatif)

Jika sudah install Docker Desktop:

```bash
# Jalankan semua service (Django + MySQL) sekaligus
docker-compose up -d

# Buat data demo
docker-compose exec web python manage.py create_demo_data
```

Akses: **http://localhost:8000**

---

## Credential Login Demo

Setelah menjalankan `create_demo_data`, gunakan akun berikut:

### Admin

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |
| Role | Admin — bisa lihat semua data, kelola karyawan, export laporan |

### Karyawan

| Username | Password | Nama | Jabatan |
|---|---|---|---|
| `budi` | `karyawan123` | Budi Santoso | Software Engineer |
| `siti` | `karyawan123` | Siti Rahayu | UI/UX Designer |
| `ahmad` | `karyawan123` | Ahmad Fauzi | Project Manager |
| `dewi` | `karyawan123` | Dewi Lestari | Marketing Specialist |
| `agus` | `karyawan123` | Agus Priyanto | Finance Staff |

---

## Struktur Database

```
accounts_user          ← Login + role (admin/employee)
      ↕ 1:1
employees_employee     ← Data profil karyawan (KRY-001, dst)
      ↕ 1:N
attendance_attendance  ← Record absensi harian + foto + GPS
```

**Logika otomatis:**
- `nomor_karyawan` di-generate otomatis: KRY-001, KRY-002, ...
- `status` absensi otomatis `terlambat` jika `jam_masuk > 08:30`
- Satu karyawan hanya bisa punya 1 record absensi per hari

---

## Struktur Folder

```
otsupresence_fixed/
├── accounts/          ← Auth: login, logout, model User custom
├── attendance/        ← Absensi: check-in, check-out, laporan, export
├── employees/         ← Karyawan: CRUD, dashboard, API
├── core/              ← Settings, URL utama, WSGI
├── templates/         ← HTML templates (responsive, mobile-first)
│   ├── accounts/      ← login.html
│   ├── attendance/    ← attendance_list.html, monthly_report.html
│   └── employees/     ← dashboard.html, employee_*.html
├── static/            ← CSS, JS, images
├── db/
│   └── schema.sql     ← Schema MySQL manual (alternatif migrate)
├── .env.example       ← Template konfigurasi environment
├── requirements.txt   ← Python dependencies
├── docker-compose.yml ← Docker setup
└── manage.py
```

---

## Deploy Online (Production)

Untuk deploy ke server publik agar bisa diakses dari internet:

### Persiapan `.env` Production

```env
SECRET_KEY=secret-key-yang-panjang-dan-random
DEBUG=False
ALLOWED_HOSTS=domain-kamu.com,www.domain-kamu.com

DB_ENGINE=mysql
DB_NAME=otsupresence_db
DB_USER=db_user_production
DB_PASSWORD=password_production_kuat
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Collectstatic

```bash
python manage.py collectstatic --noinput
```

### Rekomendasi Stack Production

| Komponen | Rekomendasi |
|---|---|
| Web server | Nginx |
| WSGI | Gunicorn (sudah ada di requirements) |
| SSL/HTTPS | Let's Encrypt (wajib untuk fitur kamera di HP) |
| Database | MySQL di server yang sama atau RDS |
| Hosting | VPS (DigitalOcean, Vultr, IDCloudHost, Niagahoster) |

> **Penting:** Fitur kamera (foto selfie) di browser smartphone **wajib HTTPS** untuk production. Tanpa SSL, browser akan memblokir akses kamera.

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'MySQLdb'`**
```bash
pip install mysqlclient
# Jika gagal di Windows:
pip install PyMySQL
```
Lalu tambahkan di `core/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

**`django.db.utils.OperationalError: (1049, "Unknown database 'otsupresence_db'")`**

Database belum dibuat. Jalankan dulu:
```sql
CREATE DATABASE otsupresence_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Kamera tidak bisa diakses dari HP**

Pastikan:
1. Server dijalankan dengan `0.0.0.0:8000` bukan `127.0.0.1:8000`
2. Gunakan Firefox di HP untuk testing (Chrome butuh HTTPS untuk kamera)
3. Atau akses via `http://localhost:8000` langsung di HP jika pakai emulator

**`collectstatic` error — folder tidak ditemukan**

Folder `static/` sudah ada di project. Jalankan:
```bash
python manage.py collectstatic --noinput
```



---

## Deploy ke Railway (MySQL)

### Credentials Demo
| Role | Email | Password |
|---|---|---|
| Admin | admin@demo.com | password123 |
| Karyawan | user@demo.com | password123 |

### Langkah Deploy
1. Buka https://railway.app → Login with GitHub
2. New Project → Deploy from GitHub repo → pilih repo ini, branch `master`
3. Add Service → Database → MySQL → tunggu Running
4. Klik service Django → Variables → tambahkan:
   - `SECRET_KEY` = (generate random key)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*.railway.app`
5. Settings → Networking → Generate Domain
6. Selesai! Akun demo otomatis dibuat saat deploy.

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
