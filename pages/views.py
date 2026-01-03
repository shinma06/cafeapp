from typing import Any
from datetime import datetime, timedelta
import calendar

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic
import jpholiday

from .models import News, Menu, Booking
from .forms import NewsForm, MenuForm, BookingForm, ContactForm


def is_superuser(user) -> bool:
    """スーパーユーザーかどうかを判定"""
    return user.is_superuser


class PaginationMixin:
    """ページネーション機能を提供するMixin"""
    
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        current_page = context['page_obj'].number
        total_pages = context['page_obj'].paginator.num_pages

        # アイテム数が10以下の場合はページネーションを表示しない
        if total_pages == 1:
            context['show_pagination'] = False
            return context

        context['show_pagination'] = True

        # ページ番号の範囲を計算
        if total_pages <= 5:
            pages = range(1, total_pages + 1)
        elif current_page <= 2:
            pages = range(1, 6)
        elif current_page >= total_pages - 1:
            pages = range(total_pages - 4, total_pages + 1)
        else:
            pages = range(current_page - 2, current_page + 3)

        context['pages'] = pages
        return context


class ReferrerRequiredMixin:
    """リファラーが必要なビューに使用するMixin"""
    
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.META.get('HTTP_REFERER'):
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)


# ホーム
class IndexView(generic.TemplateView):
    """トップページビュー"""
    template_name = 'pages/index.html'


# メニュー関連
class MenuView(generic.ListView):
    """メニュー一覧ビュー"""
    template_name = 'pages/menu.html'
    model = Menu
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category_display_names'] = dict(News.Category.choices)
        return context


class DetailMenuView(generic.TemplateView):
    """メニュー詳細ビュー"""
    template_name = 'pages/menu_detail.html'


@method_decorator(user_passes_test(is_superuser, login_url='pages:menu'), name='dispatch')
class CreateMenuView(generic.CreateView):
    """メニュー作成ビュー（スーパーユーザーのみ）"""
    template_name = 'pages/menu_create.html'
    form_class = MenuForm
    success_url = reverse_lazy('pages:menu-posted')

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        self.request.session['menu_id'] = self.object.id
        return response


class PostedMenuView(ReferrerRequiredMixin, generic.TemplateView):
    """メニュー投稿完了ビュー"""
    template_name = 'pages/menu_posted.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        menu_id = self.request.session.get('menu_id')
        if menu_id:
            context['posted_menu'] = Menu.objects.get(id=menu_id)
        return context


# ニュース関連
class NewsView(PaginationMixin, generic.ListView):
    """ニュース一覧ビュー"""
    template_name = 'pages/news.html'
    model = News
    context_object_name = 'object_list'


class NewsCategoryView(PaginationMixin, generic.ListView):
    """カテゴリー別ニュース一覧ビュー"""
    template_name = 'pages/news.html'
    model = News
    context_object_name = 'object_list'

    def get_queryset(self) -> QuerySet[News]:
        category = self.kwargs['category']
        valid_categories = [cat[0] for cat in News.Category.choices]
        if category not in valid_categories:
            raise Http404("Category does not exist")
        self.category_name = dict(News.Category.choices).get(category)
        return News.objects.filter(category=category)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category_name'] = getattr(self, 'category_name', None)
        return context


@method_decorator(user_passes_test(is_superuser, login_url='pages:news'), name='dispatch')
class CreateNewsView(generic.CreateView):
    """ニュース作成ビュー（スーパーユーザーのみ）"""
    template_name = 'pages/news_create.html'
    form_class = NewsForm
    success_url = reverse_lazy('pages:news-posted')

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        self.request.session['news_id'] = self.object.id
        return response


class PostedNewsView(ReferrerRequiredMixin, generic.TemplateView):
    """ニュース投稿完了ビュー"""
    template_name = 'pages/news_posted.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        news_id = self.request.session.get('news_id')
        if news_id:
            context['posted_news'] = News.objects.get(id=news_id)
        return context


# 予約関連
class BookingView(generic.CreateView):
    """予約作成ビュー"""
    model = Booking
    form_class = BookingForm
    template_name = 'pages/booking.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        today = datetime.now().date()
        next_day = today + timedelta(days=1)
        three_months_later = today + timedelta(days=90)
        holidays_list = [
            holiday[0] for holiday in jpholiday.between(today, three_months_later)
        ]

        context = super().get_context_data(**kwargs)
        context['next_day'] = next_day
        context['three_months_later'] = three_months_later
        context['holidays_list'] = holidays_list
        return context

    def form_valid(self, form) -> HttpResponse:
        self.request.session['booking_data'] = form.cleaned_data
        return redirect(reverse('pages:booking-confirm'))


class BookingConfirmView(ReferrerRequiredMixin, generic.TemplateView):
    """予約確認ビュー"""
    template_name = 'pages/booking_confirm.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        booking_data = self.request.session.get('booking_data')
        context = super().get_context_data(**kwargs)
        context['booking_data'] = booking_data
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        booking_data = request.session.get('booking_data')
        if not booking_data:
            return redirect('pages:booking')

        # メールの送信
        try:
            send_mail(
                'WebCafeご予約内容確認メール',
                f'ご予約者様: {booking_data["name"]}\n\n'
                f'ご来店日: {booking_data["date"]}\n\n'
                f'ご来店時間: {booking_data["time"]}\n\n'
                f'ご来客人数: {booking_data["number_of_people"]}',
                settings.EMAIL_HOST_USER,
                [booking_data['email']],
                fail_silently=False,
            )
        except Exception as e:
            # メール送信に失敗してもデータは保存する
            print(f"メール送信エラー: {e}")

        # dateとtimeを文字列からオブジェクトに変換
        booking_data['date'] = datetime.strptime(
            booking_data['date'], '%Y/%m/%d'
        ).date()
        booking_data['time'] = datetime.strptime(
            booking_data['time'], '%H:%M'
        ).time()

        # データの保存
        Booking.objects.create(**booking_data)

        # セッションからデータを削除
        del request.session['booking_data']

        return redirect('pages:booking-complete')


class BookingCompleteView(ReferrerRequiredMixin, generic.TemplateView):
    """予約完了ビュー"""
    template_name = 'pages/booking_complete.html'


class BookingListView(PaginationMixin, generic.ListView):
    """予約一覧ビュー"""
    template_name = 'pages/booking_list.html'
    model = Booking
    context_object_name = 'booking_list'


class BookingDateView(PaginationMixin, generic.ListView):
    """期間別予約一覧ビュー"""
    template_name = 'pages/booking_list.html'
    model = Booking
    context_object_name = 'booking_list'

    def get_queryset(self) -> QuerySet[Booking]:
        today = datetime.today().date()
        date = self.kwargs.get('date')

        # 期間の計算
        date_ranges = {
            'today': (today, today),
            'tomorrow': (today + timedelta(days=1), today + timedelta(days=1)),
            'this_week': (today, today + timedelta(days=(6 - today.weekday()))),
            'this_month': (
                today,
                datetime(
                    today.year,
                    today.month,
                    calendar.monthrange(today.year, today.month)[1]
                ).date()
            ),
            'next_month': self._get_next_month_range(today),
            'past_booking': (None, today - timedelta(days=1)),
        }

        start_date, end_date = date_ranges.get(date, (today, today))

        if start_date is None:
            return Booking.objects.filter(date__lte=end_date)
        return Booking.objects.filter(date__range=(start_date, end_date))

    def _get_next_month_range(self, today):
        """来月の日付範囲を取得"""
        if today.month == 12:
            start_date = datetime(today.year + 1, 1, 1).date()
            end_date = datetime(
                today.year + 1, 1,
                calendar.monthrange(today.year + 1, 1)[1]
            ).date()
        else:
            start_date = datetime(today.year, today.month + 1, 1).date()
            end_date = datetime(
                today.year, today.month + 1,
                calendar.monthrange(today.year, today.month + 1)[1]
            ).date()
        return start_date, end_date

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['selected_period'] = self.kwargs.get('date')
        return context


# お問い合わせ関連
class ContactView(generic.View):
    """お問い合わせビュー"""

    def get(self, request: HttpRequest) -> HttpResponse:
        form = ContactForm()
        return render(request, 'pages/contact.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']

            # メールの送信
            try:
                send_mail(
                    f'件名: {subject}',
                    f'本文: {message}\n\n'
                    f'お客様のお名前: {full_name}\n'
                    f'お客様のメールアドレス: {email}',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"メール送信エラー: {e}")
                # エラーが発生してもユーザーには成功画面を表示
                # 実際の運用ではログに記録するなど適切な処理を行う

            return redirect('pages:contact-complete')
        return render(request, 'pages/contact.html', {'form': form})


class ContactCompleteView(ReferrerRequiredMixin, generic.TemplateView):
    """お問い合わせ完了ビュー"""
    template_name = 'pages/contact_complete.html'
