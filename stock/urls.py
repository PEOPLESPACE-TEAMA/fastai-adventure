from stock import views
from django.urls import path, include

#app_name='stock'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('bookmark-list/', views.bookmark_list, name='bookmark_list'),
    path('market/', views.market, name='market'), # 해당 uri가 메인페이지 입니다 !!
    path('search/', views.market_list_for_search, name='market_list_for_search'), # 검색
    path('market-list-cospi/', views.market_list_cospi, name='market_list_cospi'), 
    path('market-list-cosdaq/', views.market_list_cosdaq, name='market_list_cosdaq'),
    path('market-list-nasdaq/', views.market_list_nasdaq, name='market_list_nasdaq'),
    path('stock/<stock_code>/', views.stock_detail, name='stock_detail'),
    path('question/', views.question, name='question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/create/', views.question_create, name='question_create'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('bookmart-list/alarm', views.alarm, name='alarm'),
]