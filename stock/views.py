from django.shortcuts import render
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_datareader as pdr
import datetime

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

# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
    # 위와같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로 sript() 하여 공백 제거
    # 한국거래소 사이트에서 주식종목 코드만 가져오겠다 라는 의미
    code = code.strip()
    return code

def api_test(request):
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
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

    # data frame정리. 필요한 것은 "회사명"과 "종목코드"이므로 필요없은 칼럼은 제외
    code_df = code_df[['회사명', '종목코드']]

    # data frame title 변경 '회사명' = name, 종목코드 = 'code'
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
    # 종목코드는 6자리로 구분되기때문에 0을 채워 6자리로 변경
    code_df.code = code_df.code.map('{:06d}'.format)


    # ex) 삼성전자의의 코드를 구해보겠습니다.
    code = get_code(code_df, '삼성전자')
    # yahoo의 주식 데이터 종목은 코스피는 .KS, 코스닥은 .KQ가 붙습니다.
    # 삼성전자의 경우 코스피에 상장되어있기때문에 '종목코드.KS'로 처리하도록 한다.
    code = code + '.KS'
    # get_data_yahoo API를 통해서 yahho finance의 주식 종목 데이터를 가져온다.
    df = pdr.get_data_yahoo(code, '2021-01-18', '2021-01-22') 
    # get_Data_yahoo와 download의 차이점..? get_data_yahoo도 실시간으로 불러와지는지
    # data = yf.download(tickers='UBER', period='1d', interval='60m')

    # print(df)
    # df['Close'].plot()

        return render(request, 'stock/api_test.html')