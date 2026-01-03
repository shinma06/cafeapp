# マイグレーションガイド

このガイドでは、既存の環境から新しいリファクタリング版への移行手順を説明します。

## 前提条件

- Docker Desktop がインストールされていること
- 既存のデータをバックアップしていること

## 移行手順

### 1. 既存環境の停止とバックアップ

```bash
# 既存のコンテナを停止
docker compose down

# データベースのバックアップ（重要！）
docker compose up -d mysql
docker exec -it mysql mysqldump -u root -p0103 cafeapp > backup_$(date +%Y%m%d).sql
docker compose down
```

### 2. 環境変数の設定

```bash
# サンプルファイルをコピー
cp env.sample .env

# .envファイルを編集（必要に応じて）
# 特にメール設定やシークレットキーを変更してください
```

### 3. 新環境の構築

```bash
# Dockerイメージの再ビルド
docker compose build --no-cache

# コンテナの起動
docker compose up -d

# ログを確認（問題がないか）
docker compose logs -f
```

### 4. データベースのマイグレーション

```bash
# マイグレーションの実行
docker compose exec web python manage.py migrate

# または Makefile を使用
make migrate
```

### 5. 既存データの復元（オプション）

既存のデータベースバックアップがある場合：

```bash
# バックアップファイルをコンテナにコピー
docker cp backup_YYYYMMDD.sql mysql:/tmp/

# データベースに復元
docker exec -it mysql mysql -u root -p0103 cafeapp < /tmp/backup_YYYYMMDD.sql
```

### 6. 静的ファイルの収集

```bash
docker compose exec web python manage.py collectstatic --noinput

# または
make collectstatic
```

### 7. 動作確認

1. ブラウザで http://localhost:8000 にアクセス
2. ヘルスチェックエンドポイントを確認
   - http://localhost:8000/health/
   - http://localhost:8000/ready/
   - http://localhost:8000/alive/

### 8. 管理者アカウントの確認

既存の管理者アカウントが使えない場合：

```bash
docker compose exec web python manage.py createsuperuser

# または
make createsuperuser
```

## 主な変更点

### URLの変更

以下のURLが変更されています：

- `/menu/ditail/` → `/menu/detail/` （typo修正）
- `/contact_complete/` → `/contact/complete/` （一貫性のため）
- `/accounts/setting/` → `/accounts/settings/` （複数形に統一）
- `/accounts/login_complete/` → `/accounts/login/complete/`
- `/accounts/signup_complete/` → `/accounts/signup/complete/`
- `/accounts/logout_complete/` → `/accounts/logout/complete/`
- `/accounts/rename_complete/` → `/accounts/settings/rename/complete/`

### 環境変数

以下の環境変数が新たに使用されます：

- `DJANGO_SECRET_KEY` - Djangoのシークレットキー
- `DJANGO_DEBUG` - デバッグモード（True/False）
- `DJANGO_ALLOWED_HOSTS` - 許可するホスト名（カンマ区切り）
- `DATABASE_ENGINE` - データベースエンジン
- `DATABASE_NAME` - データベース名
- `DATABASE_USER` - データベースユーザー
- `DATABASE_PASSWORD` - データベースパスワード
- `DATABASE_HOST` - データベースホスト
- `DATABASE_PORT` - データベースポート

### Dockerボリューム

データベースデータは名前付きボリューム `mysql_data` に保存されます。
以前の `./data` ディレクトリは使用されなくなります。

## トラブルシューティング

### データベース接続エラー

```bash
# MySQLコンテナのログを確認
docker compose logs mysql

# MySQLが完全に起動するまで待つ
docker compose up -d mysql
sleep 30
docker compose up -d web
```

### マイグレーションエラー

```bash
# マイグレーションをリセット（注意：データが失われる可能性があります）
docker compose exec web python manage.py migrate --fake pages zero
docker compose exec web python manage.py migrate --fake accounts zero
docker compose exec web python manage.py migrate
```

### 静的ファイルが表示されない

```bash
# 静的ファイルを再収集
docker compose exec web python manage.py collectstatic --noinput --clear
```

### ポートの競合

`.env`ファイルで以下を変更：

```
WEB_PORT=8001  # 8000から変更
MYSQL_PORT=3307  # 3306から変更
```

## ロールバック手順

問題が発生した場合、以下の手順で元に戻せます：

```bash
# 新環境を停止
docker compose down

# 古いDockerファイルに戻す（Gitを使用している場合）
git checkout HEAD~1 Dockerfile compose.yml

# 古い環境を起動
docker compose up -d

# バックアップからデータを復元
docker cp backup_YYYYMMDD.sql mysql:/tmp/
docker exec -it mysql mysql -u root -p0103 cafeapp < /tmp/backup_YYYYMMDD.sql
```

## サポート

問題が解決しない場合は、以下を確認してください：

1. Dockerのバージョン（最新版を推奨）
2. ログファイル（`docker compose logs`）
3. 環境変数の設定（`.env`ファイル）

## 移行後の推奨事項

1. **本番環境の場合**
   - `DJANGO_DEBUG=False`に設定
   - 強力な`DJANGO_SECRET_KEY`を生成
   - `DJANGO_ALLOWED_HOSTS`を適切に設定
   - データベースパスワードを変更

2. **定期的なバックアップ**
   ```bash
   # cronジョブなどで定期実行
   docker exec mysql mysqldump -u root -pYOUR_PASSWORD cafeapp > backup_$(date +%Y%m%d).sql
   ```

3. **ログの監視**
   ```bash
   # ログを定期的に確認
   make logs
   ```

4. **セキュリティアップデート**
   ```bash
   # 定期的にパッケージを更新
   docker compose build --no-cache
   docker compose up -d
   ```

