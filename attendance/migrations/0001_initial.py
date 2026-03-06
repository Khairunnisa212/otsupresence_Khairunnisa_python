import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='attendance',
                    to='employees.employee',
                )),
                ('tanggal', models.DateField()),
                ('jam_masuk', models.TimeField(blank=True, null=True)),
                ('jam_keluar', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(
                    choices=[('hadir', 'Hadir'), ('terlambat', 'Terlambat')],
                    default='hadir',
                    max_length=20,
                )),
                # Lokasi masuk
                ('lokasi_masuk', models.CharField(blank=True, max_length=255)),
                ('latitude_masuk', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude_masuk', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                # Lokasi keluar
                ('lokasi_keluar', models.CharField(blank=True, max_length=255)),
                ('latitude_keluar', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude_keluar', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                # Foto
                ('foto_masuk', models.ImageField(blank=True, null=True, upload_to='attendance_photos/masuk/')),
                ('foto_keluar', models.ImageField(blank=True, null=True, upload_to='attendance_photos/keluar/')),
                ('keterangan', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Absensi',
                'verbose_name_plural': 'Absensi',
                'ordering': ['-tanggal', '-jam_masuk'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('employee', 'tanggal')},
        ),
    ]
