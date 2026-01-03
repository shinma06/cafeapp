from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    # トップページ
    path('', views.IndexView.as_view(), name='index'),
    
    # メニュー
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('menu/detail/', views.DetailMenuView.as_view(), name='menu-detail'),
    path('menu/create/', views.CreateMenuView.as_view(), name='menu-create'),
    path('menu/posted/', views.PostedMenuView.as_view(), name='menu-posted'),
    
    # ニュース
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/category/<str:category>/', views.NewsCategoryView.as_view(), name='news-category'),
    path('news/create/', views.CreateNewsView.as_view(), name='news-create'),
    path('news/posted/', views.PostedNewsView.as_view(), name='news-posted'),
    
    # 予約
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('booking/confirm/', views.BookingConfirmView.as_view(), name='booking-confirm'),
    path('booking/complete/', views.BookingCompleteView.as_view(), name='booking-complete'),
    path('booking/list/', views.BookingListView.as_view(), name='booking-list'),
    path('booking/list/<str:date>/', views.BookingDateView.as_view(), name='booking-date'),
    
    # お問い合わせ
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/complete/', views.ContactCompleteView.as_view(), name='contact-complete'),
]
