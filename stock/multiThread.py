from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from .models import User
import time
import datetime

class EmailThread(threading.Thread):
    def __init__(self, title, contents, address):
        self.title = title
        self.contents = render_to_string('stock/mail_template_example/regular/email.html')
        self.addess = address
        threading.Thread.__init__(self)

    def run (self):
        '''
        맨 밑에 저 코드가 실행되면 이 while문 안에서 게속 비동기 처리가 진행 됨 
        wihle 문 안에서  모든 유저의 메일과 북마크 리스트를 가져와서 특정 시간마다 메일을 보내도록 구성 하면 하면 될듯
        유저가 많아서 이거 하나로 차리하기 힘들다면 유저도 인풋으로 받아서 EmailThread().start() 를 여러개 쓰면 될듯
        ex) 
        EmailThread(유저1~100).start()
        EmailThread(유저100~200).start()
        EmailThread(유저201~300).start()
        '''
        while 1:
            '''
            p = User.objects.all()
            self.addess = '블라블라@블라블라.com'
            msg = EmailMultiAlternatives(self.title, self.contents, to=[self.addess])
            msg.content_subtype = 'html'
            msg.send()
            '''
            time.sleep(1)
            print('성공 했다고 콘솔에 찍어봐')
            print(datetime.datetime.now())


#이렇게 하면 views.py 에 임포트 될때 딱 한번 실행 됨 
#views.py에서는 이거 실행하기 위해 임포트 하는거고 views.py 안에서 이 클래스를 사용할 일은 없고 사용 하려면 디자인을 바꿔야함 
EmailThread('비동기 메일 보내기 성공?','ㅇㄹㅇㄹ','ㅇㄹㅇㄹㅇ').start()



#이거를 shell 에서 한번 테스트 해봤는데 shell 에서 exit()해도 계속 실행 됨 그 cmd를 종료해야지 죽음 이게 웃긴게 ctr+c 도 안먹힘 