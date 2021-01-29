from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from .models import User, Stock
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly
# import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objs as go
import datetime

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



# api 관련 코드

stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}


# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False).strip()
    # 위와같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로 sript() 하여 공백 제거
    # 한국거래소 사이트에서 주식종목 코드만 가져오겠다 라는 의미
    return code

# download url 조합
def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type
    df = pd.read_html(download_link, header=0)[0]  # dataframe 객체 생성
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


def api_test(request) :
        
    # kospi, kosdaq 종목코드 각각 다운로드
    kospi_df = get_download_kospi()
    kosdaq_df = get_download_kosdaq()

    # data frame merge
    code_df = pd.concat([kospi_df, kosdaq_df])

    # data frame정리 
    code_df = code_df[['회사명', '종목코드']]

    # data frame title 변경 '회사명' = name, 종목코드 = 'code'
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    companys=code_df['name'].values.tolist()
    codes=code_df['code'].values.tolist()
    
    # [중요] 초기 셋팅. db삭제하고 다시 실행할 시에 주석풀고 실행시켜야 함
    # for company, code in zip(companys, codes) :
    #     if Stock.objects.filter(company_name=company).exists() :
    #         pass
    #     else :
    #         Stock.objects.create(company_name=company,stock_code=code,stock_type=code[8])


    # for company in companys :
    #     Stock.objects.filter(company_name=company).update(open~volume까지))

    # for문을 모델의 주식코드로 돌려,,,?
    # 모델에 존재하는것들은 랭킹을 나타내거나, 하루에 보여지는 것들을 할때만 유효함..(?)
    df = yf.download(tickers='005880.KS', period='1d', interval='5m')
    print(type(df))
    print(type(df.tail(1)))

    # print(df)
    # index가 마지막인,,, 거만 하나떼어서 open/high~각각 접근해서 하나씩 update하기 해보자.
    print(df.tail(1))
    print(df.tail(1).values.tolist()) # 이거다~
    print(df.info())
    # name = code[1]

   

    return render(request, 'stock/api_test.html',{'a':df} )


    





'''
아래는 그래프 그리는 것 관련한 내용임 
'''
    # #declare figure
    # fig = go.Figure()

    # #Candlestick
    # fig.add_trace(go.Candlestick(x=df.index,
    #                 open=df['Open'],
    #                 high=df['High'],
    #                 low=df['Low'],
    #                 close=df['Close'], name = 'market data'))

    # # Add titles
    # fig.update_layout(
    #     title='삼성전자 live share price evolution',
    #     yaxis_title='Stock Price (USD per Shares)')

    # # X-Axes
    # fig.update_xaxes(
    #     rangeslider_visible=True,
    #     rangeselector=dict(
    #         buttons=list([
    #             dict(count=15, label="15m", step="minute", stepmode="backward"),
    #             dict(count=45, label="45m", step="minute", stepmode="backward"),
    #             dict(count=1, label="HTD", step="hour", stepmode="todate"),
    #             dict(count=3, label="3h", step="hour", stepmode="backward"),
    #             dict(step="all")
    #         ])
    #     )
    # )

    # #Show
    # fig.show()
    # fig.write_html('test.html') # 흠... 이게 아닌디....

    # get_data_yahoo API를 통해서 yahho finance의 주식 종목 데이터를 가져온다.
    # df = pdr.get_data_yahoo(code[0], '2021-01-18', '2021-01-22') // 여기서 pdr이 쓰이네
    # get_Data_yahoo와 download의 차이점..? get_data_yahoo도 실시간으로 불러와지는지 -> download()사용하기로 함. 탕탕
    # 실시간이라기엔 20분씩 늦는것으로 확인됨..
    
    # excel 파일을 다운로드하는거와 동시에 pandas에 load하기
    # 흔히 사용하는 df라는 변수는 data frame을 의미합니다.
    # code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    # head()함수를 사용하면 date가장 최근 5줄만 리턴한다(인자에 숫자쓰면 숫자만큼 리턴). tail()은 그 반대

    # '''
    # to do list
    
    # 0. plotly에 관한 충분한 이해.. 내가 원하는 경로에 html띄우는 법..? 
    # 5. 전일비를 통해 상승률 하락률 top5를 매길 수 있을 것 같은데, 이건 stock list에서만 나타내면 될듯? + 직접 계산해야함
    #    참고) 전일비 공식 : (현재가 - 전일종가) / 전일종가 X 100..... (시간 남으면)'''