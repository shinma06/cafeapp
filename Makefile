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
	docker compose exec postgres psql -U shinma -d cafeapp

migrate:
	docker compose exec web python manage.py migrate

createsuperuser:
	docker compose exec web python manage.py createsuperuser

tailwind:
	docker build -f Dockerfile.node -t cafeapp-tailwind .
	docker run --rm -v $(PWD)/static:/app/static cafeapp-tailwind npm run build:css
	@echo "✅ Tailwind CSSをビルドしました"

clean:
	docker compose down -v
	@echo "古いコンテナ（cafe-app-*）を削除中..."
	@docker ps -a --filter "name=cafe-app" --format "{{.Names}}" | xargs -r docker rm -f 2>/dev/null || true
	docker volume prune -f

setup: clean tailwind build up
	@echo "コンテナの起動を待っています..."
	@sleep 8
	@echo "データベースの準備を待っています..."
	@timeout=30; \
	while [ $$timeout -gt 0 ]; do \
		if docker compose exec -T web python manage.py migrate 2>/dev/null; then \
			break; \
		fi; \
		echo "コンテナの準備中... (残り $$timeout 秒)"; \
		sleep 2; \
		timeout=$$((timeout - 2)); \
	done; \
	if [ $$timeout -le 0 ]; then \
		echo "⚠️  タイムアウト: 手動でマイグレーションを実行してください: make migrate"; \
		exit 1; \
	fi
	@echo ""
	@echo "✅ セットアップ完了！"
	@echo "   http://localhost:8000"
	@echo ""
	@echo "スーパーユーザー作成:"
	@echo "   make createsuperuser"
