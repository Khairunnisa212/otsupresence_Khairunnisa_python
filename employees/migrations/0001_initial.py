import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='employee_profile',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('nomor_karyawan', models.CharField(blank=True, max_length=20, unique=True)),
                ('nama', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('jabatan', models.CharField(max_length=200)),
                ('departemen', models.CharField(default='Umum', max_length=200)),
                ('tanggal_masuk', models.DateField()),
                ('status_aktif', models.CharField(
                    choices=[('aktif', 'Aktif'), ('nonaktif', 'Nonaktif')],
                    default='aktif',
                    max_length=20,
                )),
                ('foto', models.ImageField(blank=True, null=True, upload_to='employee_photos/')),
                ('telepon', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Karyawan',
                'verbose_name_plural': 'Karyawan',
                'ordering': ['-created_at'],
            },
        ),
    ]
