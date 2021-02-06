from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.hashers import check_password, make_password
class RegisterForm(UserCreationForm):
    # 회원가입 폼
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta: 
        model = User 
        fields = ['username','email']      

    def clean_confirm_password(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return data['confirm_password']


class LoginForm(AuthenticationForm):
    # 로그인 폼
    # email = forms.CharField(label='email',max_length=255)     
    password = forms.CharField(label='password',widget=forms.PasswordInput)

