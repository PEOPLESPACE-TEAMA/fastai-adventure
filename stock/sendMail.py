from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def sendMail(title, contents, adress):
    '''
    title은 제목
    contents는 메일의 내용인데 여기를 html로 넣으면 됨
    adress는 메일을 받는 사람의 주소
    '''
    #media = 'stock/mail_template_example/regular/images'
    contents = render_to_string('stock/mail_template_example/regular/email.html') #일단 이렇게 하면 메일이 html로 가기는 하는데 이미지는 안들어감 이미지 포함해서 보내는 방법을 알아내야 함 
    email = EmailMessage(title, contents, to=[adress])
    email.content_subtype = 'html'
    email.send()    