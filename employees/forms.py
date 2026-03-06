from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    create_account = forms.BooleanField(required=False, label='Buat akun login untuk karyawan ini')
    username = forms.CharField(required=False, label='Username', help_text='Kosongkan untuk otomatis dari email')
    password = forms.CharField(
        required=False,
        label='Password',
        widget=forms.PasswordInput(),
        initial='karyawan123',
        help_text='Default: karyawan123'
    )

    class Meta:
        model = Employee
        fields = ['nama', 'email', 'jabatan', 'departemen', 'tanggal_masuk', 'status_aktif', 'foto', 'telepon']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama lengkap'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@perusahaan.com'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jabatan/posisi'}),
            'departemen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama departemen'}),
            'tanggal_masuk': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status_aktif': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
        }
