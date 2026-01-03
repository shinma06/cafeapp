from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class SignupForm(forms.ModelForm):
    """ユーザー新規登録フォーム"""
    
    username = forms.CharField(
        label='ユーザー名',
        min_length=6,
        max_length=18,
        widget=forms.TextInput(attrs={
            'placeholder': 'ユーザー名を入力してください',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='パスワード',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワードを入力してください',
            'autocomplete': 'new-password'
        })
    )
    confirm_password = forms.CharField(
        label='パスワード確認',
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワードを再入力してください',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    def clean_username(self):
        """ユーザー名のバリデーション"""
        username = self.cleaned_data.get('username')
        
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('ユーザー名は半角英数字のみ有効です。')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'このユーザー名は既に使用されています。別のユーザー名を選択してください。'
            )
        
        return username

    def clean_password(self):
        """パスワードのバリデーション"""
        password = self.cleaned_data.get('password')
        
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+$', password):
            raise ValidationError('パスワードは半角英字と半角数字を組み合わせてください。')
        
        return password

    def clean(self):
        """パスワード一致確認"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('パスワードが一致しません。')
        
        return cleaned_data


class LoginForm(forms.Form):
    """ログインフォーム"""
    
    username = forms.CharField(
        label='ユーザー名',
        max_length=18,
        widget=forms.TextInput(attrs={
            'placeholder': 'ユーザー名を入力してください',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='パスワード',
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'パスワードを入力してください',
            'autocomplete': 'current-password'
        })
    )

    def clean(self):
        """ログイン認証のバリデーション"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('ユーザー名かパスワードが間違っています。')

        return cleaned_data


class RenameForm(forms.Form):
    """ユーザー名変更フォーム"""
    
    username = forms.CharField(
        label='新しいユーザー名',
        min_length=6,
        max_length=18,
        widget=forms.TextInput(attrs={
            'placeholder': '新しいユーザー名を入力してください',
            'autocomplete': 'username'
        })
    )

    def clean_username(self):
        """ユーザー名のバリデーション"""
        username = self.cleaned_data.get('username')
        
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('ユーザー名は半角英数字のみ有効です。')

        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'このユーザー名は既に使用されています。別のユーザー名を選択してください。'
            )

        return username
