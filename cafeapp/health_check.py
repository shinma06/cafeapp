"""
ヘルスチェック用のビュー
"""
from django.http import JsonResponse
from django.db import connection
from django.conf import settings


def health_check(request):
    """
    アプリケーションのヘルスチェックエンドポイント
    データベース接続を確認して、正常性を返す
    """
    try:
        # データベース接続の確認
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'debug': settings.DEBUG
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)


def readiness_check(request):
    """
    レディネスチェックエンドポイント
    アプリケーションがリクエストを受け付ける準備ができているかを確認
    """
    return JsonResponse({
        'status': 'ready'
    }, status=200)


def liveness_check(request):
    """
    ライブネスチェックエンドポイント
    アプリケーションが生存しているかを確認
    """
    return JsonResponse({
        'status': 'alive'
    }, status=200)

