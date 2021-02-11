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
    path('market-list-cospi/', views.market_list_cospi, name='market_list_cospi'), 
    path('market-list-cosdaq/', views.market_list_cosdaq, name='market_list_cosdaq'),
    path('market-list-nasdaq/', views.market_list_nasdaq, name='market_list_nasdaq'),
    path('stock/<stock_code>/', views.stock_detail, name='stock_detail'),
]