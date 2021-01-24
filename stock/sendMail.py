from django.core.mail import EmailMessage

def sendMail(title, contents, adress):
    '''
    title은 제목
    contents는 메일의 내용인데 여기를 html로 넣으면 됨
    adress는 메일을 받는 사람의 주소
    '''
    email = EmailMessage(title, contents, to=[adress])
    email.send()    