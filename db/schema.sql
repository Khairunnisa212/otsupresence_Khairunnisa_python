-- ============================================================
-- OtsuPresence Database Schema
-- PT Otsuka Indonesia | MySQL 8.0
-- ============================================================
-- Jalankan file ini di MySQL untuk membuat database secara manual
-- (alternatif dari python manage.py migrate)
--
-- Urutan eksekusi HARUS berurutan karena ada FK dependency:
--   1. accounts_user
--   2. employees_employee   (FK -> accounts_user)
--   3. attendance_attendance (FK -> employees_employee)
--   4. Tabel Django bawaan (session, admin log, dll)
-- ============================================================

CREATE DATABASE IF NOT EXISTS otsupresence_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE otsupresence_db;

-- ============================================================
-- TABEL DJANGO BAWAAN (dibutuhkan oleh AbstractUser)
-- ============================================================

CREATE TABLE IF NOT EXISTS django_content_type (
    id          INT          NOT NULL AUTO_INCREMENT,
    app_label   VARCHAR(100) NOT NULL,
    model       VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY unique_app_model (app_label, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS auth_permission (
    id              INT          NOT NULL AUTO_INCREMENT,
    name            VARCHAR(255) NOT NULL,
    content_type_id INT          NOT NULL,
    codename        VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY unique_content_codename (content_type_id, codename),
    CONSTRAINT fk_perm_content FOREIGN KEY (content_type_id)
        REFERENCES django_content_type(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS auth_group (
    id   INT          NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_group_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id            BIGINT NOT NULL AUTO_INCREMENT,
    group_id      INT    NOT NULL,
    permission_id INT    NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY unique_group_perm (group_id, permission_id),
    CONSTRAINT fk_gp_group FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    CONSTRAINT fk_gp_perm  FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 1. accounts_user
-- Extends Django AbstractUser. Menyimpan credential login
-- dan role pengguna (admin / employee).
-- ============================================================

CREATE TABLE IF NOT EXISTS accounts_user (
    id            BIGINT       NOT NULL AUTO_INCREMENT,
    password      VARCHAR(128) NOT NULL                    COMMENT 'Hashed password (PBKDF2)',
    last_login    DATETIME(6)  NULL                        COMMENT 'Timestamp login terakhir',
    is_superuser  TINYINT(1)   NOT NULL DEFAULT 0          COMMENT 'Akses superuser Django',
    username      VARCHAR(150) NOT NULL                    COMMENT 'Username unik untuk login',
    first_name    VARCHAR(150) NOT NULL DEFAULT ''         COMMENT 'Nama depan',
    last_name     VARCHAR(150) NOT NULL DEFAULT ''         COMMENT 'Nama belakang',
    email         VARCHAR(254) NOT NULL DEFAULT ''         COMMENT 'Alamat email',
    is_staff      TINYINT(1)   NOT NULL DEFAULT 0          COMMENT 'Akses Django admin panel',
    is_active     TINYINT(1)   NOT NULL DEFAULT 1          COMMENT 'Status aktif akun (0=nonaktif)',
    date_joined   DATETIME(6)  NOT NULL                    COMMENT 'Tanggal & waktu akun dibuat',
    role          VARCHAR(20)  NOT NULL DEFAULT 'employee'  COMMENT 'Role: admin / employee',
    photo         VARCHAR(255) NULL                        COMMENT 'Path file foto profil',
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='User login — extends Django AbstractUser';

CREATE TABLE IF NOT EXISTS accounts_user_groups (
    id       BIGINT NOT NULL AUTO_INCREMENT,
    user_id  BIGINT NOT NULL,
    group_id INT    NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY unique_user_group (user_id, group_id),
    CONSTRAINT fk_ug_user  FOREIGN KEY (user_id)  REFERENCES accounts_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_ug_group FOREIGN KEY (group_id) REFERENCES auth_group(id)    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS accounts_user_user_permissions (
    id            BIGINT NOT NULL AUTO_INCREMENT,
    user_id       BIGINT NOT NULL,
    permission_id INT    NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY unique_user_perm (user_id, permission_id),
    CONSTRAINT fk_up_user FOREIGN KEY (user_id)       REFERENCES accounts_user(id)  ON DELETE CASCADE,
    CONSTRAINT fk_up_perm FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 2. employees_employee
-- Data profil lengkap karyawan. Relasi 1:1 dengan accounts_user.
-- nomor_karyawan di-generate otomatis: KRY-001, KRY-002, ...
-- ============================================================

CREATE TABLE IF NOT EXISTS employees_employee (
    id              BIGINT       NOT NULL AUTO_INCREMENT,
    user_id         BIGINT       NULL                    COMMENT 'FK -> accounts_user.id (OneToOne, nullable)',
    nomor_karyawan  VARCHAR(20)  NOT NULL                COMMENT 'Auto-generate: KRY-001, KRY-002, ...',
    nama            VARCHAR(200) NOT NULL                COMMENT 'Nama lengkap karyawan',
    email           VARCHAR(254) NOT NULL                COMMENT 'Email karyawan (unik)',
    jabatan         VARCHAR(200) NOT NULL                COMMENT 'Jabatan / posisi',
    departemen      VARCHAR(200) NOT NULL DEFAULT 'Umum' COMMENT 'Nama departemen',
    tanggal_masuk   DATE         NOT NULL                COMMENT 'Tanggal mulai bekerja',
    status_aktif    VARCHAR(20)  NOT NULL DEFAULT 'aktif' COMMENT 'Status: aktif / nonaktif',
    foto            VARCHAR(255) NULL                    COMMENT 'Path foto karyawan',
    telepon         VARCHAR(20)  NOT NULL DEFAULT ''     COMMENT 'Nomor telepon',
    created_at      DATETIME(6)  NOT NULL                COMMENT 'Waktu data dibuat',
    updated_at      DATETIME(6)  NOT NULL                COMMENT 'Waktu data terakhir diupdate',
    PRIMARY KEY (id),
    UNIQUE KEY uk_nomor_karyawan (nomor_karyawan),
    UNIQUE KEY uk_email          (email),
    UNIQUE KEY uk_user_id        (user_id),
    CONSTRAINT fk_emp_user FOREIGN KEY (user_id)
        REFERENCES accounts_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Data profil karyawan';

-- ============================================================
-- 3. attendance_attendance
-- Record absensi harian. 1 karyawan = max 1 record per tanggal.
-- Status otomatis: terlambat jika jam_masuk > 08:30
-- ============================================================

CREATE TABLE IF NOT EXISTS attendance_attendance (
    id                BIGINT         NOT NULL AUTO_INCREMENT,
    employee_id       BIGINT         NOT NULL               COMMENT 'FK -> employees_employee.id',
    tanggal           DATE           NOT NULL               COMMENT 'Tanggal absensi',
    jam_masuk         TIME           NULL                   COMMENT 'Jam check-in',
    jam_keluar        TIME           NULL                   COMMENT 'Jam check-out (null jika belum)',
    status            VARCHAR(20)    NOT NULL DEFAULT 'hadir' COMMENT 'hadir / terlambat (otomatis)',
    lokasi_masuk      VARCHAR(255)   NOT NULL DEFAULT ''    COMMENT 'Nama lokasi check-in',
    latitude_masuk    DECIMAL(10,7)  NULL                   COMMENT 'Latitude check-in',
    longitude_masuk   DECIMAL(10,7)  NULL                   COMMENT 'Longitude check-in',
    lokasi_keluar     VARCHAR(255)   NOT NULL DEFAULT ''    COMMENT 'Nama lokasi check-out',
    latitude_keluar   DECIMAL(10,7)  NULL                   COMMENT 'Latitude check-out',
    longitude_keluar  DECIMAL(10,7)  NULL                   COMMENT 'Longitude check-out',
    foto_masuk        VARCHAR(255)   NULL                   COMMENT 'Path foto selfie check-in',
    foto_keluar       VARCHAR(255)   NULL                   COMMENT 'Path foto selfie check-out',
    keterangan        LONGTEXT       NULL                   COMMENT 'Catatan tambahan',
    created_at        DATETIME(6)    NOT NULL               COMMENT 'Waktu record dibuat',
    PRIMARY KEY (id),
    UNIQUE KEY uk_employee_tanggal (employee_id, tanggal),
    CONSTRAINT fk_att_employee FOREIGN KEY (employee_id)
        REFERENCES employees_employee(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Record absensi harian karyawan';

-- ============================================================
-- TABEL DJANGO BAWAAN LAINNYA
-- ============================================================

CREATE TABLE IF NOT EXISTS django_session (
    session_key  VARCHAR(40)  NOT NULL,
    session_data LONGTEXT     NOT NULL,
    expire_date  DATETIME(6)  NOT NULL,
    PRIMARY KEY (session_key),
    KEY idx_expire_date (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS django_admin_log (
    id              INT          NOT NULL AUTO_INCREMENT,
    action_time     DATETIME(6)  NOT NULL,
    object_id       LONGTEXT     NULL,
    object_repr     VARCHAR(200) NOT NULL,
    action_flag     SMALLINT     NOT NULL CHECK (action_flag >= 0),
    change_message  LONGTEXT     NOT NULL,
    content_type_id INT          NULL,
    user_id         BIGINT       NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_log_content FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE SET NULL,
    CONSTRAINT fk_log_user    FOREIGN KEY (user_id)         REFERENCES accounts_user(id)        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS django_migrations (
    id      BIGINT       NOT NULL AUTO_INCREMENT,
    app     VARCHAR(255) NOT NULL,
    name    VARCHAR(255) NOT NULL,
    applied DATETIME(6)  NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- VERIFIKASI: uncomment untuk cek tabel yang sudah dibuat
-- ============================================================
-- SELECT table_name, table_comment, table_rows
-- FROM information_schema.tables
-- WHERE table_schema = 'otsupresence_db'
-- ORDER BY table_name;
