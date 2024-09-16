from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User 
from app.models import (
   SanPham,
   DanhMuc
)
class LoginForm(forms.Form):
    username = forms.CharField(label="Tên người dùng", widget=forms.TextInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-titleSMColor placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 text-box single-line'}))
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-titleSMColor placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 text-box single-line'}))
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == "":
            raise ValidationError("Vui lòng điền vào tên người dùng!")
        return username
    

class KhachHangForm(forms.ModelForm):
    username = forms.CharField(label="Tên người dùng", widget=forms.TextInput(attrs={}))
    email = forms.EmailField(max_length=254, label="Email", widget=forms.EmailInput(attrs={}))
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput(attrs={}))
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label="Họ", widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(label="Tên", widget=forms.TextInput(attrs={}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name', 'last_name', )



class SanPhamForm(forms.ModelForm):
    danhmuc = forms.ModelChoiceField(
        queryset=DanhMuc.objects.all(),
        to_field_name='id',
        required=True,  
        widget=forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '})
    )
    class Meta:
        model = SanPham
        fields = ['ten', 'mota', 'gia', 'gioitinh','kichhoat', 'hinhanh', 'danhmuc']
        labels = {
            'ten': 'Tên',
            'mota': 'Mô tả',
            'gia': 'Giá',
            'gioitinh': 'Giới tính',
            'kichhoat': 'Kích hoạt',
            'hinhanh': 'Hình ảnh',
            'danhmuc': 'Danh mục',
        }
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}),
            'mota': forms.Textarea(attrs={'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 '}),
            'gia': forms.NumberInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}),
            'gioitinh': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '}),
            'kichhoat': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 '}),
            'hinhanh': forms.FileInput(attrs={'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none '}),
        }

class DanhMucForm(forms.ModelForm):
    class Meta:
        model = DanhMuc
        fields = ['ten']
        labels = {
            'ten': 'Tên',
        }
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}),
        }

    def clean_ten(self):
        ten = self.cleaned_data.get('ten')
        if not ten:
            raise forms.ValidationError("Trường 'ten' là bắt buộc.")
        if DanhMuc.objects.filter(ten=ten).exists():
            raise forms.ValidationError("Danh mục đã tồn tại.")
        return ten