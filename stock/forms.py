from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    # 회원가입 폼
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm password',widget=forms.PasswordInput)

    class Meta: 
        model = User 
        fields = ['username','email']      

    def clean_confirm_password(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        return data['confirm_password']


class LoginForm(forms.Form):
    # 로그인 폼
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    email = forms.CharField(label='email',max_length=255)     

    def clean(self):
        data = super.clean()
        email = data.get('email')
        password = data.get('password')
        if password and email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                self.add_error('email', '아이디가 존재하지 않습니다')
                return
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
            else:
                self.email = user.email