from typing import Any
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from .forms import SignupForm, LoginForm, RenameForm


class ReferrerRequiredMixin:
    """リファラーが必要なビューに使用するMixin"""
    
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.META.get('HTTP_REFERER'):
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)


class SignupView(generic.View):
    """ユーザー新規登録ビュー"""
    template_name = 'accounts/signup.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('pages:index')

        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('accounts:signup_complete')
        return render(request, self.template_name, {'form': form})


class SignupCompleteView(ReferrerRequiredMixin, generic.TemplateView):
    """新規登録完了ビュー"""
    template_name = 'accounts/signup_complete.html'


class LoginView(generic.View):
    """ログインビュー"""
    template_name = 'accounts/login.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('pages:index')

        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:login_complete')
            else:
                form.add_error(None, 'ユーザー名かパスワードが間違っています。')
        return render(request, self.template_name, {'form': form})


class LoginCompleteView(ReferrerRequiredMixin, generic.TemplateView):
    """ログイン完了ビュー"""
    template_name = 'accounts/login_complete.html'


class LogoutCompleteView(ReferrerRequiredMixin, generic.TemplateView):
    """ログアウト完了ビュー"""
    template_name = 'accounts/logout_complete.html'


class AccountEditView(LoginRequiredMixin, generic.View):
    """アカウント編集ビュー"""
    template_name = 'accounts/account_edit.html'
    login_url = 'accounts:login'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = RenameForm(initial={'username': request.user.username})
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = RenameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            request.user.username = new_username
            request.user.save()
            return redirect('accounts:rename_complete')

        return render(request, self.template_name, {'form': form})


class RenameCompleteView(ReferrerRequiredMixin, generic.TemplateView):
    """ユーザー名変更完了ビュー"""
    template_name = 'accounts/rename_complete.html'
