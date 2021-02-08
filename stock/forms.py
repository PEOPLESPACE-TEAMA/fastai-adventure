from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Question, Answer, Review
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.admin.widgets import AdminTimeWidget

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


class QuestionForm(forms.ModelForm):
    # 질문 작성 폼
    class Meta:
        model = Question
        fields = ['title', 'content']


class AnswerForm(forms.ModelForm):
    # 답변 작성 폼
    class Meta:
        model = Answer
        fields = ['content']


class AlarmForm(forms.ModelForm):
    # 메일 알람 시간 설정 폼
    class Meta:
        model = User
        fields = ['mail_alarm_time_hour','mail_alarm_time_minute']


class Reviewform(forms.ModelForm):
    #후기 폼
    class Meta:
        model = Review
        fields = ['title', 'content']

