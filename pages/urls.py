from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('menu/create/', views.CreateMenuView.as_view(), name='menu-create'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news/create/', views.CreateNewsView.as_view(), name='news-create'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact_complete/', views.ContactCompleteView.as_view(), name='contact_complete'),
]
