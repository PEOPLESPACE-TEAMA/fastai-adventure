from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def sendMail(title, contents, adress):
    '''
    title은 제목
    contents는 메일의 내용인데 여기를 html로 넣으면 됨
    adress는 메일을 받는 사람의 주소
    '''
    #media = 'stock/mail_template_example/regular/images'
    contents = render_to_string('stock/mail_template_example/regular/email.html') #일단 이렇게 하면 메일이 html로 가기는 하는데 이미지는 안들어감 이미지 포함해서 보내는 방법을 알아내야 함 
    email = EmailMultiAlternatives(title, contents, to=[adress])
    #email = EmailMessage(title, contents, to=[adress])
    email.content_subtype = 'html'
    email.send()    

    #이거 html로 보내기는 가능한데 html파일에 있는 이미지는 같이 안보내짐 어떻게 이미지 넣어서 html로 메일 보내는지 모르겠음
    #이미지 못 넣으면 html로 그래프를 그리는게 가능하다면 html로 그래프를 그러서 넣을수 있음녀 좋을 듯 