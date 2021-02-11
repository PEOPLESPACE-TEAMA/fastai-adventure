from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import User
from django.http import HttpResponse

# 로그인 확인
def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # messages.info(request, "로그인한 사용자만 이용할 수 있습니다.")
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrap

# 관리자 권한 확인
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.admin==True:
            return function(request, *args, **kwargs)
        return HttpResponse('관리자만 답변을 작성할 수 있습니다.')
        # return redirect('main')
    return wrap

# 비로그인 확인
def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('로그아웃 후 사용 바랍니다.')
        return function(request, *args, **kwargs)
    return wrap