from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from .models import User
from datetime import datetime
import time

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
import plotly.express as px
import plotly.graph_objs as go
import datetime
from .utils import get_plot,get_bar_graph
from django.core.paginator import Paginator
from PIL import Image
import os
import numpy as np
from django.contrib.auth import login as login_a, authenticate
from .prediction import predict, getLabels

class EmailThread(threading.Thread):
    def __init__(self, address):
        self.addess = address
        threading.Thread.__init__(self)

    def run (self):

        # while(1): 시간체크를 위해 계속 함수 실행중이어야 함..
        now = datetime.datetime.now()
        # to_do_list
        # 0. user 모델에 시간 필드 추가 후, bookmark_list페이지에서 시간 선택할 수 있도록 설정 (30m)
        # 1. self.address 통해서 현재 이 함수에서 해당유저의 bookmark랑 시간필드 가져오기 (10m)
        # 2. 시간필드가 null이면 return 0 (2m)
        # 2. 시간필드가 null이 아니면 그 시간이 now.hour랑 now.minute이 같은지 확인 (5m)
        # 3. 이미지 필드 전송하는 법 공부하기 (월요일) https://www.askcompany.kr/vod/automation/134/ (링크 참고)
        
        # cf. 단점은 이걸 runserver를 돌려야만 가능하다 ..? 근데 실재 배포를 하고 계속 서버가 돌아가면 자동으로 될듯도 하다 !
        # if now.hour == 19 and now.minute == 43 :
        title = "stock에서 은서님께 보내는 메세지 랍니다"
        contents =  "안녕안녕" # html 형식으로 보내야 깔끔할 것 같긴 함. sendMail.py 참고
        msg = EmailMultiAlternatives(title, contents, to=[self.addess])
        # msg.content_subtype = 'html'
        msg.send()

        time.sleep(1)
        print('스레드 한 개 작업 완룟')


        return 0
            
            # return 0

        # else :
        #     print(now.hour)
        #     print(now.minute)
        #     time.sleep(1)
        #     pass



#이렇게 하면 views.py 에 임포트 될때 딱 한번 실행 됨 
#views.py에서는 이거 실행하기 위해 임포트 하는거고 views.py 안에서 이 클래스를 사용할 일은 없고 사용 하려면 디자인을 바꿔야함 
# def send_email(subject, body, to_email): # 왜 이거하면 안되냐 ? 


# 4. user 객체 만큼  for문 돌리기 
EmailThread("rhdmstj1740@gmail.com").start() # 하나씩 쓰레드를 실행시키는 것임.. #start()가 run메서드를 호출하는 것임.
# EmailThread('비동기 메일 보내기 네번째','여긴내용입니다','rhdmstj1740@gmail.com').start()


#이거를 shell 에서 한번 테스트 해봤는데 shell 에서 exit()해도 계속 실행 됨 그 cmd를 종료해야지 죽음 이게 웃긴게 ctr+c 도 안먹힘 