from django.contrib import admin
from .models import News, Menu, Review, Booking


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """ニュース管理画面設定"""
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'text']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """メニュー管理画面設定"""
    list_display = ['title', 'price', 'created_at']
    search_fields = ['title']
    ordering = ['-created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """レビュー管理画面設定"""
    list_display = ['title', 'user', 'product', 'rating', 'date_posted']
    list_filter = ['rating', 'date_posted']
    search_fields = ['title', 'content', 'user__username']
    date_hierarchy = 'date_posted'
    ordering = ['-date_posted']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """予約管理画面設定"""
    list_display = ['name', 'date', 'time', 'number_of_people', 'phone_number', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['name', 'email', 'phone_number']
    date_hierarchy = 'date'
    ordering = ['-date', '-time']
