from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from django.views.generic import View
from .models import User, Stock, Bookmark
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import plotly
from functools import wraps
# import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objs as go
import datetime
from .utils import get_plot
from django.core.paginator import Paginator
from PIL import Image
import os
import numpy as np
from django.contrib.auth import login, authenticate
from .prediction import predict, getLabels

def main(request):
    return render(request, 'stock/main.html')

def signup(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()
            useremail = user_form.cleaned_data.get('email')
            userpw = user_form.cleaned_data['password']
            user.username = user_form.cleaned_data.get('username')
            user.email=useremail
            user.set_password(userpw)
            user.save()
            user = authenticate(email = useremail,password=userpw) 
            # 회원가입이 성공적으로 되면 로그인 페이지로 이동
            return redirect('login')
    else:
        user_form = RegisterForm()
    return render(request, 'stock/signup.html',{'form': user_form})

def login(request):
    if request.method =='POST':
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            return redirect('home')
    else:
        user_form = LoginForm()
    return render(request, 'stock/login.html',{'form': user_form})

def logout(request):
    # 로그아웃 하면 로그인 화면으로 연결
    return render(request, 'stock/login.html')

def home(request):
    stocks = Stock.objects.all().order_by('-id')
    # user = User.objects.get(username = request.user.username)

    # increase, decrease 계산하려면 아래 주석 풀기
    # 계산이 오래 걸려요. 한 번 계산되면 다시 주석 설정해도 됩니다!
    # for stock in stocks:
    #     try:
    #         stock.initialize()
    #         stock.calculate_rate()
    #     except:
    #         pass
    q = request.POST.get('q', "") 
    if q:
        search = stocks.filter(company_name__icontains=q)
        return render(request, 'stock/search.html', {'stocks' : search, 'q' : q})
    bookmarks = stocks.filter(bookmarked=True).order_by('?')
    increases = stocks.exclude(increase=None).order_by('-increase')[:5]
    decreases = stocks.exclude(decrease=None).order_by('decrease')[:5]

    bookmark = bookmarks[0];    top = increases[0];    bottom = decreases[0]
    bookmarkchart = draw_chart(bookmark)
    increasechart = draw_chart(top)
    decreasechart = draw_chart(bottom)

    return render(request, 'stock/home.html', {'bookmarks': bookmarks, 'increases': increases, 'decreases': decreases, 
            'bookmarkchart': bookmarkchart, 'increasechart': increasechart, 'decreasechart': decreasechart})

def crop_image(self,stock):
    graph = Image.open(self)
    pattern=graph.crop((850,40,945,400)) # left, up, right, down 95*360
    stock_name = stock.company_name
    path = "./graphimg/"
    pattern.save(path+stock.company_name+'crop.PNG')
    rgb_im = pattern.convert('RGB')
    pix = np.array(rgb_im)
    stop = False
    r, g, b = rgb_im.getpixel((90, 180))
    for i in range(0, 360):
        for j in range(0, 95):
            r, g, b = rgb_im.getpixel((j, i))
            if r < 200:
                stop = True
                break
        if stop == True:
            break
    top = i
    stop = False
    for i in range(359, 0, -1):
        for j in range(94, 0, -1):
            r, g, b = rgb_im.getpixel((j, i))
            if r < 200:
                stop = True
                break
        if stop == True:
            break
    bottom = i
    pattern=graph.crop((850,40+top,945,40+bottom))
    pattern.show()
    pattern.save(path+stock.company_name+'newcrop.PNG')

def bookmark(request):
    return render(request, 'stock/bookmark.html')

def bookmark_list(request):
    if request.user.is_authenticated:
        print('로그인 되어 있네')
    else:
        print('dkdlsp')
    #슈퍼계정으로 로그인 하면 로그인 되어 있다고 함 근데 일반 계정으로 로그인 하면 로그인 안되어 있다고 함 

    #print(request.user)
    user = User.objects.get(username = 'dongjun') #유저네임 바꾸기 이 로그인 에러 있어서 일단 이렇게 했는데 레어 없으면 username = request.user.username 이나 그냥 현재 로그인 유저를 특정 할수 있게 하면 됨 
    bookmark = Bookmark.objects.filter(user = user)

    return render(request, 'stock/bookmark_list.html',{'bookmark':bookmark})

#이거는 그냥 테스트 해볼려고 만든거 
def addbookmark(user,stock):
    # user = User.objects.get(username=name)
    print(user)
    bookmark = Bookmark()
    bookmark.user = user
    bookmark.stock = stock
    print(bookmark)
    bookmark.save()


def market(request):
    return render(request, 'stock/market.html')

def market_list(request):
    stocks = Stock.objects.all().order_by('company_name')
    paginator = Paginator(stocks, 20)
    page = request.GET.get("page",'1')
    posts = paginator.get_page(page)

    today = datetime.date.today()  
    yesterday = today - datetime.timedelta(1)  
    str_yesterday = str(yesterday)

    context = {'posts':posts, 'today':today}

    # 하루 지날때마다 업데이트 하기
    # for stock in stocks :
    #     stock_code=stock.stock_code
    #     try:
    #         pass
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

    #     except:
    #         pass

    # 업데이트2 ( 등락율, 등락폭 ) 
    # incrase랑 decrease는 데이터를 싹 다 비우고 해야겠네

    # for stock in stocks :
    #     stock.calculate_rate()
    #     stock.calculate_width()
        
    return render(request, 'stock/market_list.html', context )
 

def stock_detail(request,stock_code):
    print(request.user)
    stocks = Stock.objects.get(stock_code = stock_code)
    stock_list = Stock.objects.all().order_by('-id')
    increases = stock_list.exclude(increase=None).order_by('-increase')[:5]
    decreases = stock_list.exclude(decrease=None).order_by('decrease')[:5]
    chart = draw_chart(stocks)
    vals = {'시가':stocks.open,'고가':stocks.high,'저가':stocks.low,'거래량':stocks.volume,'수정주가':stocks.adj_close}
    
    # imgForPrediction= crop_image(stocks.chart_image)
    crop_image(stocks.chart_image,stocks)
    img_path = "./graphimg/"+stocks.company_name+'newcrop.PNG'
    predictedLabel,predictedIdx,probability = predict(img_path)
    predictedProbability = round(float(probability[int(predictedIdx)])*100,2)
    print(predictedLabel)

    #북마크에 저장
    if request.method == 'POST':
        print(request.user)
        print(stocks)
        addbookmark(request.user,stocks)
    
    return render(request, 'stock/stock_detail.html',{'companyName':stocks.company_name, 'vals': vals,'chart':chart,'decreases': decreases,'increases': increases,'predictedLabel':predictedLabel,'probability':predictedProbability})

def draw_chart(self):
    stock_code = self.stock_code
    df = yf.download(tickers=stock_code, period='1d', interval='2m')
    size = int(df.size/6) 
    print(size)
    data = df.values.tolist()
    time = df.index.tolist()
    x=[];    y=[]
    for i in time:
        time_only = i.strftime("%H:%M:%S")
        print("time:", time_only)
        x.append(i)
    for index in range(0,size):
        y.append(data[index][3])
    chart = get_plot(x,y)
    fig = plt.gcf()
    path = "./graphimg/"
    if not os.path.isdir(path):                                                           
        os.mkdir(path)
    fig.savefig(path+self.company_name+'.png', dpi=fig.dpi)
    self.chart_image = path+self.company_name+'.png'
    self.save()
    return chart


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
    
    # [중요] 초기 셋팅. db삭제하거나 sqlite파일 gitignore에 있는데 pull할 시에, 아래 주석풀고 실행시켜야 함
    # create하고 나선 다시 주석처리..
    # for company, code in zip(companys, codes) :
    #     if Stock.objects.filter(company_name=company).exists() :
    #         pass
    #     else :
    #         Stock.objects.create(company_name=company,stock_code=code,stock_type=code[8])

    return render(request, 'stock/api_test.html',  )


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
    
    