from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

from .models import News, Menu, Booking


class NewsForm(forms.ModelForm):
    """ニュース作成フォーム"""
    
    category = forms.ChoiceField(
        label='カテゴリー',
        choices=News.Category.choices,
        required=True
    )

    class Meta:
        model = News
        fields = ['category', 'title', 'text', 'img', 'alt']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        img = cleaned_data.get('img')
        alt = cleaned_data.get('alt')

        if img and not alt:
            raise ValidationError(
                '画像が指定されている場合は画像タイトルも入力してください。'
            )
        if not img and alt:
            raise ValidationError(
                '画像が指定されていない場合は画像タイトルを指定することはできません。'
            )

        return cleaned_data


class MenuForm(forms.ModelForm):
    """メニュー作成フォーム"""
    
    class Meta:
        model = Menu
        fields = ['title', 'img', 'alt', 'price']
        widgets = {
            'price': forms.NumberInput(attrs={'min': '0'}),
        }


class BookingForm(forms.ModelForm):
    """予約作成フォーム"""
    
    # 営業時間の選択肢を生成（9:30〜21:00、30分刻み）
    HOURS_CHOICES = [
        (f"{h:02}:{m:02}", f"{h:02}:{m:02}")
        for h in range(9, 22)
        for m in [0, 30]
        if not ((h == 21 and m == 30) or (h == 9 and m == 0))
    ]

    date = forms.CharField(
        label="日付",
        widget=forms.TextInput(attrs={
            'id': 'datepicker',
            'readonly': 'readonly'
        })
    )
    time = forms.ChoiceField(
        label="時間",
        choices=[('', '-----')] + HOURS_CHOICES,
        required=True
    )
    number_of_people = forms.IntegerField(
        label="人数",
        initial=1,
        widget=forms.NumberInput(attrs={
            'min': '1',
            'max': '10'
        })
    )

    class Meta:
        model = Booking
        fields = ['name', 'date', 'time', 'email', 'phone_number', 'number_of_people']

    def clean_date(self):
        """日付のバリデーション"""
        date_str = self.cleaned_data['date']
        
        try:
            date_obj = datetime.strptime(date_str, '%Y/%m/%d').date()
        except ValueError:
            raise ValidationError("日付はyyyy/mm/dd形式で入力してください。")
        
        return date_obj

    def _post_clean(self):
        """dateフィールドをyyyy/mm/dd形式の文字列として返す"""
        super()._post_clean()
        if 'date' in self.cleaned_data:
            self.cleaned_data['date'] = self.cleaned_data['date'].strftime('%Y/%m/%d')


class ContactForm(forms.Form):
    """お問い合わせフォーム"""
    
    subject = forms.CharField(
        label='件名',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': '件名を入力してください'
        })
    )
    message = forms.CharField(
        label='本文',
        widget=forms.Textarea(attrs={
            'rows': 8,
            'placeholder': 'お問い合わせ内容を入力してください'
        })
    )
    full_name = forms.CharField(
        label='フルネーム',
        max_length=40,
        widget=forms.TextInput(attrs={
            'placeholder': '山田 太郎'
        })
    )
    email = forms.EmailField(
        label='メールアドレス',
        max_length=40,
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@example.com'
        })
    )
