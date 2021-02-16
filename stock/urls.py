from stock import views
from django.urls import path, include

#app_name='stock'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('bookmark-list/', views.bookmark_list, name='bookmark_list'),
    path('home/', views.home, name='home'), # 해당 uri가 메인페이지 입니다 !!
    path('search/', views.market_list_for_search, name='market_list_for_search'), # 검색
    path('market-list-kospi/', views.market_list_kospi, name='market_list_kospi'), 
    path('market-list-nasdaq/', views.market_list_nasdaq, name='market_list_nasdaq'),
    path('stock/<stock_code>/', views.stock_detail, name='stock_detail'),
    path('question/', views.question, name='question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/create/', views.question_create, name='question_create'),
    path('bookmark-list/alarm', views.alarm, name='alarm'),
    path('review/', views.review, name = 'review'),

    # patterns_list uri c추가!
    path('patterns_list', views.patterns_list, name = 'patterns_list'),

    # 새로운 템플릿 동작 확인용
    path('home/',views.home, name='home'),
    path('forgot/',views.forgot, name='forgot-password'),
    path('guideline/',views.guideline, name='guideline'),
    path('aboutus/',views.aboutus, name='aboutus'),
    path('review_create/',views.review_create, name='review_create'),
    path('qnalist/',views.qnalist, name='qnalist'), 
    path('qnacreate/',views.qnacreate, name='qnacreate'), 

]