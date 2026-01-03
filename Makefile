.PHONY: help build up down restart logs shell dbshell migrate createsuperuser clean setup tailwind

help:
	@echo "Cafe App 開発コマンド"
	@echo ""
	@echo "  make build          - Dockerイメージをビルド"
	@echo "  make up             - コンテナを起動"
	@echo "  make down           - コンテナを停止"
	@echo "  make restart        - コンテナを再起動"
	@echo "  make logs           - ログを表示"
	@echo "  make shell          - Webコンテナのシェル"
	@echo "  make dbshell        - PostgreSQLシェル"
	@echo "  make migrate        - マイグレーション実行"
	@echo "  make createsuperuser - スーパーユーザー作成"
	@echo "  make tailwind       - Tailwind CSSをビルド"
	@echo "  make clean          - すべて削除"
	@echo "  make setup          - 初期セットアップ"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

shell:
	docker compose exec web bash

dbshell:
	docker compose exec postgres psql -U shinma -d cafe_app

migrate:
	docker compose exec web python manage.py migrate

createsuperuser:
	docker compose exec web python manage.py createsuperuser

tailwind:
	docker build -f Dockerfile.node -t cafe-app-tailwind .
	docker run --rm -v $(PWD)/static:/app/static cafe-app-tailwind npm run build:css
	@echo "✅ Tailwind CSSをビルドしました"

clean:
	docker compose down -v
	docker volume prune -f

setup: clean tailwind build up
	@echo "データベースの準備を待っています..."
	@sleep 5
	@docker compose exec web python manage.py migrate
	@echo ""
	@echo "✅ セットアップ完了！"
	@echo "   http://localhost:8000"
	@echo ""
	@echo "スーパーユーザー作成:"
	@echo "   make createsuperuser"
