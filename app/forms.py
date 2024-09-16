from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, label="Email", widget=forms.EmailInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}))
    username = forms.CharField(label="Tên người dùng", widget=forms.TextInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}))
    password1 = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}))
    password2 = forms.CharField(label="Xác nhận mật khẩu", widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email này đã được sử dụng. Vui lòng nhập email khác!")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Tên người dùng này đã được sử dụng. Vui lòng nhập tên khác!")
        return username
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class LoginForm(forms.Form):
    username = forms.CharField(label="Tên người dùng", widget=forms.TextInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}))
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md py-2 px-1 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-400 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-green-300 sm:text-sm sm:leading-6'}))
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == "":
            raise ValidationError("Vui lòng điền vào tên người dùng!")
        return username
