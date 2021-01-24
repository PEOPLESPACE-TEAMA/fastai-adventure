from django.shortcuts import render
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_datareader as pdr
import datetime
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
            login_form = LoginForm()
            # 회원가입이 성공적으로 되면 로그인 페이지로 이동
            return render(request, 'stock/login.html',{'form': login_form})
    else:
        user_form = RegisterForm()
    return render(request, 'stock/signup.html',{'form': user_form})

def login(request):
    if request.method =='POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            return render(request, 'stock/home.html')
    else:
        user_form = LoginForm()
    return render(request, 'stock/login.html',{'form': user_form})

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


stock_type = {
        'kospi' : 'stockMkt',
        'kosdaq' : 'kosdaqMkt'
}
    

# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
    # 위와같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로 sript() 하여 공백 제거
    # 한국거래소 사이트에서 주식종목 코드만 가져오겠다 라는 의미
    code = code.strip()
    return code, name

# download url 조합
def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type
    df = pd.read_html(download_link, header=0)[0]
    return df

# kospi 종목코드 목록 다운로드
def get_download_kospi():
    df = get_download_stock('kospi')
    # '종목코드.KS'로 처리하도록 한다.
    df.종목코드 = df.종목코드.map('{:06d}.KS'.format)
    return df

# kosdaq 종목코드 목록 다운로드
def get_download_kosdaq():
    df = get_download_stock('kosdaq')
    # '종목코드.KS'로 처리하도록 한다.
    df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)
    return df


def api_test(request):
    
    
    # kospi, kosdaq 종목코드 각각 다운로드
    kospi_df = get_download_kospi()
    kosdaq_df = get_download_kosdaq()

    # data frame merge
    code_df = pd.concat([kospi_df, kosdaq_df])

    # data frame정리 , 필요한 것은 "회사명"과 "종목코드"이므로 필요없은 칼럼은 제외
    code_df = code_df[['회사명', '종목코드']]


    # data frame title 변경 '회사명' = name, 종목코드 = 'code'
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
    # 종목코드는 6자리로 구분되기때문에 0을 채워 6자리로 변경
    # code_df.code = code_df.code.map('{:06d}'.format)


    # ex) 삼성전자의의 코드를 구해보기
    code = list(get_code(code_df, '삼성전자')) 


    # get_data_yahoo API를 통해서 yahho finance의 주식 종목 데이터를 가져온다.
    # df = pdr.get_data_yahoo(code[0], '2021-01-18', '2021-01-22') 
    # get_Data_yahoo와 download의 차이점..? get_data_yahoo도 실시간으로 불러와지는지
    df = yf.download(tickers=code[0], period='10d', interval='5m')
    
    name = code[1]

    
    return render(request, 'stock/api_test.html' , {'df' : df, 'a': name})



    '''
    #Data viz
    import plotly.graph_objs as go

    data = yf.download(tickers='UBER', period='1d', interval='60m')
    #Print data
    print(data)
    print(type(list(data)))'''

    # https://ai-creator.tistory.com/51 (참고자료)

    
    # excel 파일을 다운로드하는거와 동시에 pandas에 load하기
    # 흔히 사용하는 df라는 변수는 data frame을 의미합니다.
    # code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    # head()함수를 사용하면 date가장 최근 5줄만 리턴한다. tail()은 그 반대

    '''
    to do list
    1. 주식종목name을 한국거래소에서 list를 뽑아와서 txt파일에 저장한 다음에 파이썬 리스트에 한꺼번에 넣어서,
       for loop 활용하여 download하기 -> stock detail에 들어갈 부분 (화요일)
    2. list가 보여지고 detail로 들어가는 걸 db에 넣지 않고 구현할 수 있을지 고민 ... (이게 제일 고민쓰)
       충분히 고민해보기 (화요일)
    3. matplotlib으로 나타내기 (수요일)
    4. 전일비를 통해 상승률 하락률 top5를 매길 수 있을 것 같은데, 이건 stock list에서만 나타낼 수 있을듯? + 직접 계산해야함
       참고) 전일비 공식 : (현재가 - 전일종가) / 전일종가 X 100... 화이팅... (시간 남으면 )'''