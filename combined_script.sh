#!/bin/bash

# エラー時に終了し、未定義変数の使用を防ぐ
set -euo pipefail

# カラー出力の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# MySQLの起動を待機
wait_for_mysql() {
    log_info "Waiting for MySQL to be ready..."
    local max_retries=30
    local retry_count=0
    
    until nc -z mysql 3306; do
        retry_count=$((retry_count + 1))
        if [ $retry_count -ge $max_retries ]; then
            log_error "MySQL is not available after ${max_retries} attempts. Exiting."
            exit 1
        fi
        log_warn "MySQL is unavailable - sleeping (attempt ${retry_count}/${max_retries})"
        sleep 2
    done
    
    log_info "MySQL is up and ready!"
}

# Djangoサーバーの起動
start_server() {
    log_info "Starting Django development server..."
    python3 manage.py runcontainer
}

# メイン処理
main() {
    # MySQLの準備を待つ
    wait_for_mysql
    
    # サーバーを起動（クラッシュ時は自動再起動）
    while true; do
        if start_server; then
            log_info "Server stopped normally."
            break
        else
            log_error "Server crashed with exit code $?. Restarting in 5 seconds..."
            sleep 5
        fi
    done
}

# スクリプトの実行
main
