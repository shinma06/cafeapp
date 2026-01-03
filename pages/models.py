from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class News(models.Model):
    """ニュース記事モデル"""
    
    class Category(models.TextChoices):
        """ニュースカテゴリー"""
        EMPTY = '', 'カテゴリーを選択'
        PROMOTION = 'promotion', 'お店の紹介'
        IRREGULAR_MENU = 'irregularmenu', '期間限定メニュー'
        EVENT = 'event', 'イベント'
        TALK = 'talk', 'お客様との会話'
    
    category = models.CharField(
        max_length=100,
        choices=Category.choices,
        verbose_name='カテゴリー'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='タイトル'
    )
    text = models.TextField(
        verbose_name='本文'
    )
    img = models.ImageField(
        null=True,
        blank=True,
        upload_to='news/',
        verbose_name='画像'
    )
    alt = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='画像タイトル'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='作成日時'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ニュース'
        verbose_name_plural = 'ニュース'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title


class Menu(models.Model):
    """メニューモデル"""
    
    title = models.CharField(
        max_length=50,
        verbose_name='メニュー名'
    )
    img = models.ImageField(
        upload_to='menu/',
        verbose_name='メニュー画像'
    )
    alt = models.CharField(
        max_length=50,
        verbose_name='画像タイトル'
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='値段(円)'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='作成日時'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'メニュー'
        verbose_name_plural = 'メニュー'
    
    def __str__(self):
        return self.title


class Review(models.Model):
    """レビューモデル"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ユーザー'
    )
    product = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='商品'
    )
    date_posted = models.DateTimeField(
        auto_now_add=True,
        verbose_name='投稿日時'
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='評価'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='タイトル'
    )
    content = models.TextField(
        verbose_name='本文'
    )

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー'

    def __str__(self):
        return f'{self.title} - {self.user.username}'


class Booking(models.Model):
    """予約モデル"""
    
    name = models.CharField(
        max_length=40,
        verbose_name='名前'
    )
    date = models.DateField(
        verbose_name='日付'
    )
    time = models.TimeField(
        verbose_name='時間'
    )
    email = models.EmailField(
        max_length=40,
        null=True,
        verbose_name='メールアドレス'
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='電話番号'
    )
    number_of_people = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='人数'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='作成日時'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = '予約'
        verbose_name_plural = '予約'
        indexes = [
            models.Index(fields=['date', 'time']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.name} - {self.date} {self.time}'
