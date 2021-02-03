from django.shortcuts import render,redirect
from .forms import RegisterForm, LoginForm
from .models import User, Stock
import pandas as pd
import pandas_datareader as pdr
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
    stocks = Stock.objects.all().order_by('-id')
    # increase, decrease 계산하려면 아래 주석 풀고 테스트
      # for stock in stocks:
    #     stock.initialize()
    #     stock.calculate_rate()
    q = request.POST.get('q', "") 
    if q:
        search = stocks.filter(company_name__icontains=q)
        return render(request, 'stock/search.html', {'stocks' : search, 'q' : q})
    bookmarks = stocks.filter(bookmarked=True)
    increases = stocks.exclude(increase=None).order_by('increase')[:5]
    decreases = stocks.exclude(decrease=None).order_by('decrease')[:5]
    return render(request, 'stock/home.html',{'bookmarks': bookmarks, 'increases': increases, 'decreases': decreases})

def bookmark(request):
    return render(request, 'stock/bookmark.html')

def bookmark_list(request):
    return render(request, 'stock/bookmark_list.html')

def market(request):
    return render(request, 'stock/market.html')

def market_list(request):
    # sort alphabetically 
    stocks = Stock.objects.all().order_by('id')

    # 하루 지날때마다 업데이트 하기 (시가~전일종가) (30분 소요)
    today = datetime.date.today()  
    yesterday = today - datetime.timedelta(1)  
    str_yesterday = str(yesterday)
    
    for stock in stocks :
        stock_code=stock.stock_code
        try:
            pass
            # df = yf.download(tickers=stock_code, period='1d', interval='5m')
            # lists = df.tail(1).values.tolist()
            # stock.open=lists[0][0]
            # stock.high=lists[0][1]
            # stock.low=lists[0][2]
            # stock.close=lists[0][3]
            # stock.adj_close=lists[0][4]
            # stock.volume=lists[0][5]

            # before_df = pdr.get_data_yahoo(stock_code, str_yesterday, str_yesterday)
            # before_lists=before_df.values.tolist()
            # stock.before_close=before_lists[0][3]

            # stock.save()
        except:
            pass

    # 업데이트 ( 등락율, 등락폭 ) 
    for stock in stocks :
        # open만 계속 업데이트해서 등락율, 등락폭 바로 바로 갱신해도 괜찮을듯?
        stock.calculate_rate()
        stock.calculate_width()

    return render(request, 'stock/market_list.html', { 'stocks' : stocks , 'str':str_yesterday} )

def stock_detail(request,stock_code):
    stocks = Stock.objects.get(stock_code = stock_code)
    labels = ['stock_type','open','high','low','close','adj_close','volume']
    data = [stocks.stock_type,stocks.open,stocks.high,stocks.low,stocks.close,stocks.adj_close,stocks.volume]

    vals = {'시가':stocks.open,'고가':stocks.high,'저가':stocks.low,'거래량':stocks.volume}
    print(vals)
    return render(request, 'stock/stock_detail.html',{'companyName':stocks.company_name, 'vals': vals})



#### 아래는 모두 야후 파이낸스 api 불러왔던 코드 ( 이젠 쓸 일 없음 - 나중에 별도 파일로 뺄게요,,! )

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


def just_test() :
        
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
    
    # [중요] 초기 셋팅. db삭제하거나 sqlite파일 gitignore에 있는데 pull할 시에, 아래 주석풀고 실행시켜야 함
    # create하고 나선 다시 주석처리..
    # for company, code in zip(companys, codes) :
    #     if Stock.objects.filter(company_name=company).exists() :
    #         pass
    #     else :
    #         Stock.objects.create(company_name=company,stock_code=code,stock_type=code[8])


'''
아래는 그래프 그리는 것 관련한 내용임 (구냥 구글링) (반응형 차트)
'''
    # import plotly.graph_objs as go

    # df = yf.download(tickers='특정종목의 주식코드', period='1d', interval='5m')

    # fig = go.Figure()      
    # #Candlestick (캔들차트)
    # fig.add_trace(go.Candlestick(x=df.index,
    #                 open=df['Open'],
    #                 high=df['High'],
    #                 low=df['Low'],
    #                 close=df['Close'], name = 'market data'))

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
    # fig.write_html('test.html') # 흠... 이게 아닌디.... 이미지로 저장해야한다.

    # df = pdr.get_data_yahoo(code[0], '2021-01-18', '2021-01-22') // 여기서 pdr이 쓰이네
    # get_Data_yahoo와 download의 차이점..? get_data_yahoo도 실시간으로 불러와지는지 -> download()사용하기로 함. 탕탕
    # 실시간이라기엔 20분씩 늦음 
    
    