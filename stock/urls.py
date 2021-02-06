from stock import views
from django.urls import path, include

#app_name='stock'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('bookmark-list/', views.bookmark_list, name='bookmark_list'),
    path('market/', views.market, name='market'), # 기존에 있던 home이 여기에 통합되었습니당 ! 이 uri가 메인페이지 입니다 !!
    path('market-list/', views.market_list, name='market_list'), # list를 각 마켓별로 보여준다면,, 아마 동일한 url 3개 필요할 듯 
    path('stock/<stock_code>/', views.stock_detail, name='stock_detail'),
    path('search/', views.market, name='search'), # 전체 리스트 url로 넘어가야 할 듯 하다
]