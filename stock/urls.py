from stock import views
from django.urls import path, include

#app_name='stock'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('bookmark/', views.bookmark, name='bookmark'), # 비회원 북마크
    path('bookmark/<int:user_id>/', views.bookmark, name='bookmark'), # 회원 북마크
    path('bookmark-list/', views.bookmark_list, name='bookmark_list'),
    path('bookmark-list/<int:user_id>/', views.bookmark_list, name='bookmark_list'),
    path('market/', views.market, name='market'),
    path('market-list/', views.market_list, name='market_list'),
    path('stock/<int:pk>/', views.stock_detail, name='stock_detail'),
    path('api_test/', views.api_test, name='api_test'),
]