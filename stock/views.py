from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, QuestionForm, AnswerForm,Reviewform
from django.views.generic import View

from .models import User, Stock, Bookmark, Question, Answer, News, Review, StockIndex
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import plotly
from functools import wraps
import plotly.express as px
import plotly.graph_objs as go
import datetime
from .utils import get_plot,get_bar_graph
from django.core.paginator import Paginator
from PIL import Image
import os
import numpy as np
from django.contrib.auth import login as login_a, authenticate
from django.contrib import auth
from .prediction import predict, getLabels
import requests
import json
from django.utils import timezone
from stock.decorators import *
import FinanceDataReader as fdr
import time
from django.shortcuts import render_to_response
from django.db import IntegrityError

#from .multiThread import EmailThread #비동기 메일 처리 기능 사용하는 사람만 주석 풀고 사용하세요. 테스트 끝나고 푸시 할때는 다시 주석처리 해주세요.

def main(request):
    # kospi_initial_data_create()
    # nasdaq_initial_data_create()
    # data_update_short()
    return render(request, 'stock/main.html')

# 새로운 템플릿 확인용 주소 시작
def aboutus(request):
    return render(request, 'stock/AboutUs.html')

def guideline(request):
    return render(request, 'stock/guideline.html')

def reviewcreate(request):
    return render(request, 'stock/review_create.html')

def reviewlist(request):
    return render(request, 'stock/review_list.html')

def qnacreate(request):
    return render(request, 'stock/qnaCreate.html')

def qnalist(request):
    return render(request, 'stock/qnaList.html')

# 새로운 템플릿 확인용 주소 끝   


def signup(request):
    errorMsg=""
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            try:
                user=user_form.save(commit=False)
                user.email = user_form.cleaned_data.get('email')
                user.save()
            except IntegrityError as e:
                return render(request,"stock/signup.html", {'form': user_form,"message": "You already have an account with this email"})             
            # 회원가입이 성공적으로 되면 로그인 페이지로 이동
            return redirect('login')
            # errorMsg = "There is an account with this email already!"
    else:
        user_form = RegisterForm()
    return render(request, 'stock/signup.html',{'form': user_form})

@logout_message_required
def login(request):
    if request.method =='POST':
        user_form = LoginForm(request,request.POST)
        if user_form.is_valid():
            login_a(request, user_form.get_user(), backend='django.contrib.auth.backends.ModelBackend') 
            return redirect('home')
        else:
           return render(request,"stock/login.html", {'form': user_form,"message": "Please check your email and password again"}) 
    else:
        user_form = LoginForm()
    return render(request, 'stock/login.html',{'form': user_form})

def logout(request):
    # 로그아웃 하면 로그인 화면으로 연결
    auth.logout(request)
    return redirect('login')

def home(request):
    stocks = Stock.objects.all().order_by('-id')
   
    # 각 종목들 update하려면 (전일종가와 오늘시가 갱신(long) -> 상승률/하락율 등락폭 갱신(short) ) 아래 주석 풀기
    # data_update_long()
    # data_update_short()
    
    q = request.POST.get('q', "") 
    if q:
        stocks=Stock.objects.all().exlude(stock_type='SS').exclude(stock_type='NN')
        search = stocks.filter(company_name__icontains=q)
        context ={
            'stocks':search,
        }
        return render(request, 'stock/market_list_for_search.html', context)

    bm_list = []
    try:
        bookmarks = Bookmark.objects.filter(user=request.user)
        for bm in bookmarks:
            bm_list.append(bm)
    except:
        pass
    bookmarks = stocks.filter(company_name__in=bm_list)
    increases = stocks.exclude(increase=None).order_by('-increase')[:5]
    decreases = stocks.exclude(decrease=None).order_by('decrease')[:5]
    
    updateNews()
    news = News.objects.all()

    # 매일 자정 코스피,나스닥 주가 지수 그래프 업데이트하고 싶을때 아래 주석 풀기!!
    # kospi=update_draw_chart_for_home('KS11','kospi')
    # nasdaq=update_draw_chart_for_home('IXIC','nasdaq')

    # 매일 자정 코스피,나스닥 시세정보 업데이트하고 싶을때 아래 주석 풀기 !!
    # stock_index('KS11','kospi')
    # stock_index('IXIC','nasdaq')

    kospidetail = StockIndex.objects.filter(stock_type="kospi")
    nasdaqdetail = StockIndex.objects.filter(stock_type="nasdaq")

    context = {
        'bookmarks': bookmarks,
        'increases': increases,
        'decreases': decreases,
        'kospidetails':kospidetail,
        'nasdaqdetails':nasdaqdetail,
        'news': news,
    }
    return render(request, 'stock/home.html', context)

def stock_index(stock,stock__type) :
    stockindexs =StockIndex.objects.filter(stock_type=stock__type)
    for stockindex in stockindexs :
        stockindex.stock_type=stock__type
        today=datetime.date.today()
        stockindex.updated_date=today
        df = fdr.DataReader(stock, today)
        tuple = df.shape
        i=1
        if tuple[0]==0 :
            while tuple[0]==0 :
                before_day = today - datetime.timedelta(i)  
                df = fdr.DataReader(stock, before_day, before_day)
                tuple = df.shape
                i=i+1
            stockindex.updated_date = today - datetime.timedelta(i-1) 
        lists = df.values.tolist()
        stockindex.close=lists[0][0]
        stockindex.open=lists[0][1]
        stockindex.high=lists[0][2]
        stockindex.low=lists[0][3]
        stockindex.volume=lists[0][4]
        stockindex.change=lists[0][5]

        stockindex.save()



def market_list_for_search(request):
    q = request.POST.get('q', "") 
    if q:
        stocks=Stock.objects.all()
        search = stocks.filter(company_name__icontains=q)
        context ={
            'stocks':search,
        }
        return render(request, 'stock/market_list_for_search.html', context)
    else :
        return render(request, 'stock/market_list_for_search.html')

def crop_image(self,stock):
    graph = Image.open(self)
    pattern=graph.crop((850,40,945,400)) # left, up, right, down 95*360
    stock_name = stock.company_name
    path = "./graphimg/"
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
    pattern=graph.crop((850,35+top,945,45+bottom))
    # pattern.show()
    pattern.save(path+stock.company_name+'crop.PNG')


def bookmark(request):
    return render(request, 'stock/bookmark.html')


def alarm(request):
    
    if request.method == "POST":
        hour=request.POST['hour']
        minute=request.POST['minute']

        user = request.user
        user.mail_alarm_time_hour = hour
        user.mail_alarm_time_minute = minute
        user.save()
        print(user)
        print(user.email)
        print(user.username)
        # form = AlarmForm(request.POST, instance=request.user)
        # if form.is_valid():
        #     a=form.save(commit=False)
        #     a.user=request.user
        #     a.save()
        #     print(user)
        #     print(user.email)
        #     print(user.username)
        #     # user.mail_alarm_time_hour = form.mail_alarm_time_hour
        #     # user.mail_alarm_time_minute = form.mail_alarm_time_minute
        #     # user.save()
        return redirect('bookmark_list')
    else:
        # form = AlarmForm()
        context = {
            # 'form':form,
        }
    return render(request, 'stock/alarm.html', context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def bookmark_list(request):
    if request.user.is_authenticated:
        print('로그인 성공')
        print(request.user)
        print(request.user.username)
    else:
        #로그인 되어 있지 않으면 로그인 페이지로 이동 
        return redirect('login')


    bookmarks = Bookmark.objects.all().filter(user=request.user)
    print(bookmarks)

    return render(request, 'stock/bookmark_list.html',{'bookmarks':bookmarks, } )


def bookmarkInOut(user,stock):
    # user = User.objects.get(username=name)
    #print(user,stock)
    bookmark = Bookmark.objects.filter(user=user,stock=stock)
    #print(bookmark)
    if len(bookmark)>0:
        bookmark.delete()
    else:
        bookmark = Bookmark()
        bookmark.user = user
        bookmark.stock = stock
        bookmark.save()

def patterns_list_nasdaq(request):
    nasdaqs=Stock.objects.filter(stock_type='N')
    
    # 매 자정 예측 data update ( 라벨이름이 바뀌어서 꼭 주석 풀고 한 번씩 진행해주세요!! )
    # nasdaq200s=Stock.objects.filter(stock_type='N').order_by('open')[:200]
    # for nasdaq200 in nasdaq200s :
    #     try:
    #         save_patterns(nasdaq200)
    #     except ValueError :
    #         pass
    #     except KeyError :
    #         pass

    
    increases=nasdaqs.filter(increase_or_decrease="increase")

    doublebottom=increases.filter(last_pattern="DoubleBottom").order_by('-predict_percentage')[:5]
    inverseheadandshoulders=increases.filter(last_pattern="InverseHeadAndShoulders").order_by('-predict_percentage')[:5]
    reversalfallingwedge=increases.filter(last_pattern="ReversalFallingWedge").order_by('-predict_percentage')[:5]
    continuousfalling=increases.filter(last_pattern="ContinuousFalling").order_by('-predict_percentage')[:5]

    decreases=nasdaqs.filter(increase_or_decrease="decrease")

    doubletop=decreases.filter(last_pattern="DoubleTop").order_by('-predict_percentage')[:5]
    headandshoulders=decreases.filter(last_pattern="HeadAndShoulders").order_by('-predict_percentage')[:5]
    reversalrisingwedge=decreases.filter(last_pattern="ReversalRisingWedge").order_by('-predict_percentage')[:5]
    continuousrising=decreases.filter(last_pattern="ContinuousRising").order_by('-predict_percentage')[:5]

    context ={
        'doublebottom':doublebottom,
        'headandshoulder':headandshoulders,
        'reversalfallingwedge':reversalfallingwedge,
        'continuousfalling':continuousfalling,

        'doubletop':doubletop,
        'inverseheadandshoulder': inverseheadandshoulders,
        'reversalrisingwedge': reversalrisingwedge,
        'continuousrising': continuousrising,
    }
    
    return render(request, 'stock/patterns_list_nasdaq.html', context=context)


def patterns_list_kospi(request):

    kospis=Stock.objects.filter(stock_type='S')
    
    # 매 자정 예측 data update ( 라벨이름이 바뀌어서 꼭 주석 풀고 한 번씩 진행해주세요!! )
    # kospi200s=Stock.objects.filter(stock_type='S').order_by('open')[:200]
    # for kospi200 in kospi200s :
    #     try:
    #         save_patterns(kospi200)
    #     except ValueError :
    #         pass
    #     except KeyError :
    #         pass


    increases=kospis.filter(increase_or_decrease="increase")

    doublebottom=increases.filter(last_pattern="DoubleBottom").order_by('-predict_percentage')[:5]
    inverseheadandshoulders=increases.filter(last_pattern="InverseHeadAndShoulders").order_by('-predict_percentage')[:5]
    reversalfallingwedge=increases.filter(last_pattern="ReversalFallingWedge").order_by('-predict_percentage')[:5]
    continuousfalling=increases.filter(last_pattern="ContinuousFalling").order_by('-predict_percentage')[:5]

    decreases=kospis.filter(increase_or_decrease="decrease")

    doubletop=decreases.filter(last_pattern="DoubleTop").order_by('-predict_percentage')[:5]
    headandshoulders=decreases.filter(last_pattern="HeadAndShoulders").order_by('-predict_percentage')[:5]
    reversalrisingwedge=decreases.filter(last_pattern="ReversalRisingWedge").order_by('-predict_percentage')[:5]
    continuousrising=decreases.filter(last_pattern="ContinuousRising").order_by('-predict_percentage')[:5]

    context ={
        'doublebottom':doublebottom,
        'headandshoulder':headandshoulders,
        'reversalfallingwedge':reversalfallingwedge,
        'continuousfalling':continuousfalling,

        'doubletop':doubletop,
        'inverseheadandshoulder': inverseheadandshoulders,
        'reversalrisingwedge': reversalrisingwedge,
        'continuousrising': continuousrising,
    }
    
    return render(request, 'stock/patterns_list_kospi.html', context=context)




def save_patterns(stock):
    # stock = Stock.objects.get(stock_code = stock_code)
    chart = draw_chart(stock)

    df = yf.download(tickers=stock.stock_code, period='1d', interval='5m')

    crop_image(stock.chart_image,stock)

    img_path = "./graphimg/"+stock.company_name+'crop.PNG'
    #모델 예측
    predictedLabel,predictedIdx,probability = predict(img_path)
    

    print("예측라벨 :", predictedLabel)
    print("상승또는하락 ", getIncreaseDecreaseResult(predictedLabel))
    print("예측확률:", round(float(probability[int(predictedIdx)])*100,2))

    stock.last_pattern = predictedLabel
    stock.increase_or_decrease = getIncreaseDecreaseResult(predictedLabel)
    stock.predict_percentage = round(float(probability[int(predictedIdx)])*100,2)
    # sign = stock.increase_or_decrease
    stock.save()


# 하기전에 pip3 install newsapi 해주세용!
def updateNews():
    url = ('http://newsapi.org/v2/everything?'
        'q=stock&'
       'sources=bbc-news&'
       'sortBy=publishedAt&'
       'apiKey=19397c8c5dfa44858d9696e3b498b1ee')
    response = requests.get(url)
    jsonResult=response.json()
    articles = jsonResult['articles'][0:5]
    for i in range(0,5):
        try:
            news = News.objects.get(newsId=i)
        except News.DoesNotExist:
            news = News()
        news.newsId=i
        news.author = articles[i]['author']
        news.title = articles[i]['title']
        news.description = articles[i]['description']
        news.redirectUrl = articles[i]['url']
        news.newsImage = articles[i]['urlToImage']
        datePublished=datetime.datetime.strptime(articles[i]['publishedAt'],"%Y-%m-%dT%H:%M:%SZ")
        news.publishedAt=datePublished
        news.save()
    print(articles)


def market_list_kospi(request):
    # 데이터 생성 및 업데이트 할 시에만 주석 풀기
    # initial_data_create()
    # data_update_long()
    # data_update_short()
    q = request.POST.get('q', "") 
    if q:
        stocks=Stock.objects.all()
        search = stocks.filter(company_name__icontains=q).filter(stock_type='S')
        context ={
            'stocks':search,
        }
        return render(request, 'stock/market_list_for_search.html', context )

    print(request.user)
    # user=User.objects.all().filter(user=request.user)

    stocks = Stock.objects.all().filter(stock_type='S').order_by('company_name')
    paginator = Paginator(stocks, 20)
    page = request.GET.get("page",'1')
    posts = paginator.get_page(page)
    # 마켓리스트에 상승률하락률 추가
    increases = stocks.exclude(increase=None).order_by('-increase')[:5]
    decreases = stocks.exclude(decrease=None).order_by('decrease')[:5]

    context = {'posts':posts, 
               'increases': increases,
               'decreases': decreases,
     }

    return render(request, 'stock/market_list_kospi.html' ,    context)
 
def market_list_kosdaq(request):
    pass

def market_list_nasdaq(request):
    # 데이터 생성 및 업데이트 할 시에만 주석 풀기
    # initial_data_create()
    # data_update_long()
    # data_update_short()
    q = request.POST.get('q', "") 
    if q:
        stocks=Stock.objects.all()
        search = stocks.filter(company_name__icontains=q).filter(stock_type='N')
        context ={
            'stocks':search,
        }
        return render(request, 'stock/market_list_for_search.html', context )

    print(request.user)
    # user=User.objects.all().filter(user=request.user)

    stocks = Stock.objects.all().filter(stock_type='N').order_by('company_name')
    paginator = Paginator(stocks, 20)
    page = request.GET.get("page",'1')
    posts = paginator.get_page(page)

    # 마켓리스트에 상승률하락률 추가
    increases = stocks.exclude(increase=None).order_by('-increase')[:5]
    decreases = stocks.exclude(decrease=None).order_by('decrease')[:5]

    context = {'posts':posts, 
               'increases': increases,
               'decreases': decreases,
     }
    
    return render(request, 'stock/market_list_nasdaq.html' ,    context)



def stock_detail(request,stock_code):
    print(request.user)
    stock = Stock.objects.get(stock_code = stock_code)

    chart = draw_chart(stock)

    df = yf.download(tickers=stock_code, period='1d', interval='5m')
    lists = df.tail(1).values.tolist()
    stock_open=lists[0][0]
    stock_high=lists[0][1] 
    stock_low=lists[0][2] 
    # stock_close=lists[0][3] 
    stock_adj_close=lists[0][4] 
    stock_volume=lists[0][5] 

    vals = {'Present price':stock_open,'High price':stock_high,'Low price':stock_low,'Trading volume':stock_volume,'Adjusted stock price average':stock_adj_close}
    # open이 진짜 찐 시가가 아니여서 임의로 현재가로 바꿔봄..

    crop_image(stock.chart_image,stock)
    img_path = "./graphimg/"+stock.company_name+'crop.PNG'
    #모델 예측
    predictedLabel,predictedIdx,probability = predict(img_path)
    #label_list = ['Bearish Pennant', 'Bearish Rectangle', 'Bullish Pennant', 'Bullish Rectangle', 'Double Bottom', 'Double Top', 'Head and Shoulders', 'Inverse Head and Shoulders', 'Continuous Falling Wedge', 'Continuous Rising Wedge', 'Reversal Falling Wedge', 'Reversal Rising Wedge']
    label_list = ['Continuous Falling', 'Continuous Rising', 'Double Bottom', 'Double Top', 'Head and Shoulders', 'Inverse Head and Shoulders', 'Reversal FallingWedge', 'Reversal RisingWedge']
    print(predictedLabel)
    print(getLabels())
    # 클라스마다 percentage로 바 그래프 만들기 
    bar_chart = draw_bar_chart(stock,probability,label_list)
    predictedProbability = round(float(probability[int(predictedIdx)])*100,2)
    label = label_list[predictedIdx]
    sign = getIncreaseDecreaseResult(predictedLabel)

    stock.last_pattern = predictedLabel
    stock.predict_percentage=predictedProbability
    stock.increase_or_decrease = getIncreaseDecreaseResult(predictedLabel)
    stock.save()

    try:
        bookmark_exist = Bookmark.objects.all().filter(user=request.user,stock=stock)
    except:
        bookmark_exist = ''

    #북마크에 저장
    if request.method == 'POST':
        print(request.user)
        print(stock)
        bookmarkInOut(request.user,stock)
        print("북마크 저장됨")
 
    return render(request, 'stock/stock_detail.html',{'companyName':stock.company_name, 'vals': vals,'chart':chart,'predictedLabel':label,'probability':predictedProbability,'bar_chart':bar_chart,'sign':sign,'bookmark_exist':bookmark_exist})

def getIncreaseDecreaseResult(predictedLabel):
    increase = ['ContinuousFalling',  'DoubleBottom','InverseHeadAndShoulders', 'ReversalFallingWedge']
    if predictedLabel in increase:
        return 'increase'
    else:
        return 'decrease'

        
  


def draw_bar_chart(self,probability,label_list):
    prob_list =[]
    print(label_list)
    for i in probability:
        prob_list.append(float(i))
    print(prob_list)
    bar_chart = get_bar_graph(label_list,prob_list)
    fig = plt.gcf()
    path = "./graphimg/"
    fig.savefig(path+self.company_name+"barchart"+'.png', dpi=fig.dpi)
    return bar_chart

def draw_chart(self):
    stock_code = self.stock_code
    df = yf.download(tickers=stock_code, period='1d', interval='2m')
    size = int(df.size/6) 
    print(size)
    data = df.values.tolist()
    time = df.index.tolist()
    x=[]
    y=[]
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


def question(request):
    question_list = Question.objects.order_by('-create_date')
    context = {
        'question_list': question_list,
    }
    return render(request, 'stock/question.html', context)

def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {
        'question': question,
        'user': request.user,
        'form': form,
    }
    return render(request, 'stock/question_detail.html', context)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'stock/question_create.html', {'form': form})

def review(request):
    #사용자 후기 게시판 
    review_list = Review.objects.all().order_by('-create_date')

    if request.method == 'POST':
       pass 
       #딜리트 어떻게 연결 해야하는지 어렵네
       #if request.user == 

    context = {
        'review_list' : review_list,
    }

    return render(request, 'stock/review.html',context)

def review_create(request):
    
    if not request.user.is_authenticated:
        return redirect(login)

    if request.method == 'POST':
        form = Reviewform(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.create_date = timezone.now()
            review.save()
            return redirect('review')
    
    form = Reviewform()
    context = {
        'form' : form,
    }

    return render(request, 'stock/review_create.html',context)




### 업데이트 함수들 

def data_update_long() :

    # 하루 지날때마다 업데이트 하기 1
    today = datetime.date.today()  
    today = datetime.date.today() - datetime.timedelta(3)
    yesterday = today - datetime.timedelta(4)  
    str_yesterday = str(yesterday)

    stocks = Stock.objects.all().filter(stock_type='N')

    for stock in stocks :
        stock_code=stock.stock_code
        # if stock.open :
        #     pass
        # else :
        try:
            df = yf.download(tickers=stock_code, period='1d', interval='60m')
            lists = df.tail(1).values.tolist()
            stock.open=lists[0][0]
            # stock.high=lists[0][1] 
            # stock.low=lists[0][2] 
            # stock.close=lists[0][3] 
            # stock.adj_close=lists[0][4] 
            # stock.volume=lists[0][5] 
            before_df = pdr.get_data_yahoo(stock_code, str_yesterday, str_yesterday)
            # Sleep(1)
            before_lists=before_df.values.tolist() 
            stock.before_close=before_lists[0][3]   
            stock.save()

        except:
            print("실패")
            pass
            


def data_update_short() :
    # 업데이트2 ( 등락율, 등락폭 ) 
    stocks = Stock.objects.all().filter(stock_type='N')
    for stock in stocks :
        try:
            stock.initialize()
            stock.calculate_rate()
            stock.calculate_width()
        except :
            pass



def update_draw_chart_for_home(self,stock_market):
    #  오늘로부터 한달
    today=datetime.date.today()
    before_month = today - datetime.timedelta(30)  
    df = fdr.DataReader(self, before_month)
    size = int(df.size/6) 
    print(size)
    data = df.values.tolist()
    time = df.index.tolist()
    x=[]
    y=[]
    for i in time:
        time_only = i.strftime("%H:%M:%S")
        print("time:", time_only)
        x.append(i)
    for index in range(0,size):
        y.append(data[index][0])
    chart = get_plot(x,y)
    fig = plt.gcf()
    path = "./stock/templates/static/stock_market/"
    if not os.path.isdir(path):                                                           
        os.mkdir(path)
    fig.savefig(path+stock_market+'.png', dpi=fig.dpi)
    print("정상 작동!")


#### 아래는 모두 야후 파이낸스 api 불러왔던 코드 (코스닥 제외)

stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}


# # 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
# def get_code(df, name):
#     code = df.query("name=='{}'".format(name))['code'].to_string(index=False).strip()
#     # 위와같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로 sript() 하여 공백 제거
#     # 한국거래소 사이트에서 주식종목 코드만 가져오겠다 라는 의미
#     return code

# download url 조합
def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type
    df = pd.read_html(download_link, header=0)[0]  # dataframe 객체 생성
    return df


# kospi 종목코드 목록 다운로드 (5000개 이상 있으나 업데이트가 너무 느려 1000개만 받아오기로 함..)
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


def kospi_initial_data_create() :
        
    # kospi, kosdaq 종목코드 각각 다운로드
    kospi_df = get_download_kospi()
    kosdaq_df = get_download_kosdaq()

    # data frame merge
    # code_df = pd.concat([kospi_df, kosdaq_df])

    # data frame정리 
    kospi_df = kospi_df[['회사명', '종목코드']]

    # data frame title 변경 '회사명' = name, 종목코드 = 'code'
    kospi_df = kospi_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    companys=kospi_df['name'].values.tolist()
    codes=kospi_df['code'].values.tolist()
    
    # create하고 나선 다시 주석처리..
    # 폐지종목 일일이 삭제해야함..
    for company, code in zip(companys, codes) :
        if Stock.objects.filter(company_name=company).exists() :
            pass
        else :
            Stock.objects.create(company_name=company,stock_code=code,stock_type=code[8])


# finance-data-reader test
def kosdaq_initial_data_create() :

    stocks = fdr.StockListing('KOSDAQ')

    # data frame정리 
    stocks = stocks[['Name', 'Symbol']]
    # stocks.Symbol = stocks.Symbol.map('{:06d}.KQ'.format)
    stocks.Symbol = stocks.Symbol+'.KQ'

    companys = stocks['Name'].values.tolist()
    codes = stocks['Symbol'].values.tolist()

    for company, code in zip(companys, codes) :
        if Stock.objects.filter(company_name=company).exists() :
            pass
        else :
            Stock.objects.create(company_name=company,stock_code=code,stock_type=code[8])


def nasdaq_initial_data_create() :

    stocks = fdr.StockListing('NASDAQ')

    # data frame정리 
    stocks = stocks[['Name', 'Symbol']]

    companys = stocks['Name'].values.tolist()
    codes = stocks['Symbol'].values.tolist()

    for company, code in zip(companys, codes) :
        if Stock.objects.filter(company_name=company).exists() :
            pass
        else :
            Stock.objects.create(company_name=company,stock_code=code,stock_type='N')


    




