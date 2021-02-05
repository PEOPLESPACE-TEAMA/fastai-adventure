from stock import views
from django.urls import path, include

#app_name='stock'

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('bookmark-list/', views.bookmark_list, name='bookmark_list'),
    path('market/', views.market, name='market'),
    path('market-list/', views.market_list, name='market_list'),
    path('stock/<stock_code>/', views.stock_detail, name='stock_detail'),
    path('search/', views.home, name='search'),
]