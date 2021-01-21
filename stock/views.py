from django.shortcuts import render


def main(request):
    return render(request, 'stock/main.html')

def signup(request):
    return render(request, 'stock/signup.html')

def login(request):
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