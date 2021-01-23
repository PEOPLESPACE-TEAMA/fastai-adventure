from django.shortcuts import render
from .forms import RegisterForm, LoginForm

def main(request):
    return render(request, 'stock/main.html')

def signup(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit = False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            # 회원가입이 성공적으로 되면 로그인 페이지로 이동
            return render(request, 'stock/login.html')
    else:
        user_form = RegisterForm()
    return render(request, 'stock/signup.html')

def login(request):
    if request.method =='POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            return render(request, 'stock/home.html')
    else:
        user_form = LoginForm()
    return render(request, 'stock/login.html')

def logout(request):
    # 로그아웃 하면 로그인 화면으로 연결
    return render(request, 'stock/login.html')

def home(request):
    return render(request, 'stock/home.html')

def bookmark(request):
    return render(request, 'stock/bookmark.html')

def bookmark_list(request):
    return render(request, 'stock/bookmark_list.html')

def market(request):
    return render(request, 'stock/market.html')

def market_list(request):
    return render(request, 'stock/market_list.html')

def stock_detail(request):
    return render(request, 'stock/stock_detail.html')