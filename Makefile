.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser test clean collectstatic

# デフォルトターゲット
help:
	@echo "CafeApp 開発コマンド"
	@echo ""
	@echo "使用可能なコマンド:"
	@echo "  make build          - Dockerイメージをビルド"
	@echo "  make up             - コンテナを起動（バックグラウンド）"
	@echo "  make down           - コンテナを停止して削除"
	@echo "  make restart        - コンテナを再起動"
	@echo "  make logs           - ログを表示"
	@echo "  make logs-f         - ログをリアルタイムで表示"
	@echo "  make shell          - Webコンテナのシェルに入る"
	@echo "  make dbshell        - MySQLシェルに入る"
	@echo "  make migrate        - マイグレーションを実行"
	@echo "  make makemigrations - マイグレーションファイルを作成"
	@echo "  make createsuperuser - スーパーユーザーを作成"
	@echo "  make collectstatic  - 静的ファイルを収集"
	@echo "  make test           - テストを実行"
	@echo "  make clean          - 停止してボリュームも削除"
	@echo "  make ps             - コンテナの状態を確認"

# Dockerイメージをビルド
build:
	docker compose build

# コンテナを起動（バックグラウンド）
up:
	docker compose up -d

# コンテナを停止して削除
down:
	docker compose down

# コンテナを再起動
restart:
	docker compose restart

# ログを表示
logs:
	docker compose logs

# ログをリアルタイムで表示
logs-f:
	docker compose logs -f

# Webコンテナのシェルに入る
shell:
	docker compose exec web bash

# MySQLシェルに入る
dbshell:
	docker compose exec mysql mysql -u root -p

# Djangoシェル
django-shell:
	docker compose exec web python manage.py shell

# マイグレーションを実行
migrate:
	docker compose exec web python manage.py migrate

# マイグレーションファイルを作成
makemigrations:
	docker compose exec web python manage.py makemigrations

# スーパーユーザーを作成
createsuperuser:
	docker compose exec web python manage.py createsuperuser

# 静的ファイルを収集
collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

# テストを実行
test:
	docker compose exec web python manage.py test

# テストをverboseモードで実行
test-v:
	docker compose exec web python manage.py test --verbosity=2

# コンテナの状態を確認
ps:
	docker compose ps

# 停止してボリュームも削除
clean:
	docker compose down -v

# 完全クリーンアップ（イメージも削除）
clean-all:
	docker compose down -v --rmi all

# 初期セットアップ
setup: build up migrate
	@echo "セットアップが完了しました！"
	@echo "http://localhost:8000 でアクセスできます"
	@echo ""
	@echo "管理者アカウントを作成するには:"
	@echo "  make createsuperuser"

# 開発環境の再構築
rebuild: clean build up migrate
	@echo "環境の再構築が完了しました！"

