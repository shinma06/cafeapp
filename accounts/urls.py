from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'accounts'

urlpatterns = [
    # ログイン・ログアウト
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/complete/', views.LoginCompleteView.as_view(), name='login_complete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/complete/', views.LogoutCompleteView.as_view(), name='logout_complete'),
    
    # 新規登録
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/complete/', views.SignupCompleteView.as_view(), name='signup_complete'),
    
    # アカウント設定
    path('settings/', views.AccountEditView.as_view(), name='account'),
    path('settings/rename/complete/', views.RenameCompleteView.as_view(), name='rename_complete'),
]
