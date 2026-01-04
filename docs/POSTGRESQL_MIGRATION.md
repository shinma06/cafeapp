# PostgreSQL移行ドキュメント

## 概要

プロジェクトのデータベースをMySQLからPostgreSQLに移行しました。この変更により、マイグレーションエラーの問題が解決され、より安定したデータベース環境が提供されます。

## 移行の理由

1. **マイグレーションエラーの解決**
   - MySQLでの`Table 'auth_permission' already exists`エラーが頻発
   - クリーンインストール時の問題を根本的に解決

2. **PostgreSQLの利点**
   - より堅牢なトランザクション管理
   - JSONBなどの高度なデータ型のサポート
   - 優れた同時実行性制御
   - オープンソースコミュニティの強力なサポート

## 変更されたファイル

### 1. `requirements.txt`
```python
# 変更前
mysqlclient>=2.2.4,<2.3.0

# 変更後
psycopg2-binary>=2.9.9,<3.0.0
```

### 2. `docker-compose.yml`
- サービス名: `mysql` → `postgres`
- イメージ: `mysql:8.0` → `postgres:16-alpine`
- ポート: `3306` → `5432`
- ボリューム名: `mysql_data` → `postgres_data`
- 環境変数:
  - `MYSQL_*` → `POSTGRES_*`
- ヘルスチェック:
  - `mysqladmin ping` → `pg_isready`

### 3. `cafeapp/settings.py`
```python
# 変更前
'ENGINE': 'django.db.backends.mysql'
'HOST': 'mysql'
'PORT': '3306'
'OPTIONS': {
    'charset': 'utf8mb4',
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
}

# 変更後
'ENGINE': 'django.db.backends.postgresql'
'HOST': 'postgres'
'PORT': '5432'
'OPTIONS': {
    'connect_timeout': 10,
}
```

### 4. `combined_script.sh`
- 関数名: `wait_for_mysql()` → `wait_for_postgres()`
- 接続先: `mysql:3306` → `postgres:5432`

### 5. `env.sample`
```bash
# 変更前
MYSQL_DATABASE=cafeapp
MYSQL_USER=shinma
MYSQL_PASSWORD=0103
MYSQL_ROOT_PASSWORD=0103
MYSQL_PORT=3306

# 変更後
POSTGRES_DB=cafeapp
POSTGRES_USER=shinma
POSTGRES_PASSWORD=0103
POSTGRES_PORT=5432
```

### 6. `Dockerfile`
```dockerfile
# 変更前
default-libmysqlclient-dev

# 変更後
libpq-dev
```

### 7. `Makefile`
```makefile
# 変更前
dbshell:
	docker compose exec mysql mysql -u root -p

# 変更後
dbshell:
	docker compose exec postgres psql -U shinma -d cafeapp
```

## 移行手順

### 既存環境からの移行

1. **データのバックアップ（必要に応じて）**
   ```bash
   # MySQLからデータをダンプ（移行前に実行する場合）
   docker compose exec mysql mysqldump -u root -p cafeapp > backup.sql
   ```

2. **完全クリーンアップ**
   ```bash
   # すべてのコンテナとボリュームを削除
   make clean
   
   # または
   docker compose down -v
   ```

3. **新しい環境のセットアップ**
   ```bash
   # イメージのビルドと起動
   make setup
   ```

4. **スーパーユーザーの作成**
   ```bash
   make createsuperuser
   ```

### PostgreSQLの特徴

#### データベースシェルへの接続
```bash
# Makefile経由
make dbshell

# 直接実行
docker compose exec postgres psql -U shinma -d cafeapp
```

#### よく使うpsqlコマンド
```sql
-- データベース一覧
\l

-- テーブル一覧
\dt

-- テーブル詳細
\d テーブル名

-- クエリ実行
SELECT * FROM auth_user;

-- 終了
\q
```

## パフォーマンス最適化

PostgreSQLは以下の点で最適化されています：

1. **接続タイムアウト設定**
   - `connect_timeout: 10` で接続の待機時間を制限

2. **ヘルスチェック**
   - 起動時間: 10秒（MySQLの20秒から短縮）
   - より高速な起動と安定性

3. **Alpine Linuxベース**
   - `postgres:16-alpine` を使用し、イメージサイズを削減

## トラブルシューティング

### 問題: PostgreSQLに接続できない

**解決方法:**
```bash
# PostgreSQLの状態を確認
docker compose ps postgres

# PostgreSQLのログを確認
docker compose logs postgres

# ヘルスチェックの状態を確認
docker compose ps
```

### 問題: マイグレーションエラー

**解決方法:**
```bash
# 完全クリーンアップ
make clean

# ボリュームを手動で削除
docker volume ls | grep postgres
docker volume rm cafeapp_postgres_data

# 再セットアップ
make setup
```

### 問題: 既存のMySQLデータを移行したい

**解決方法:**
1. MySQLからデータをエクスポート（JSON形式）
   ```bash
   docker compose exec web python manage.py dumpdata > data.json
   ```

2. PostgreSQL環境をセットアップ
   ```bash
   make clean
   make setup
   ```

3. データをインポート
   ```bash
   docker compose exec web python manage.py loaddata data.json
   ```

## 環境変数

PostgreSQL環境で使用する環境変数：

```bash
# データベース設定
POSTGRES_DB=cafeapp           # データベース名
POSTGRES_USER=shinma          # ユーザー名
POSTGRES_PASSWORD=0103        # パスワード
POSTGRES_PORT=5432            # ポート番号

# Django設定（自動的に設定される）
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=${POSTGRES_DB}
DATABASE_USER=${POSTGRES_USER}
DATABASE_PASSWORD=${POSTGRES_PASSWORD}
DATABASE_HOST=postgres
DATABASE_PORT=5432
```

## 注意事項

1. **MySQLの設定ファイルは不要**
   - `docker/mysql/conf.d/` ディレクトリは使用されません
   - 削除しても問題ありません

2. **文字コード**
   - PostgreSQLはデフォルトでUTF-8を使用
   - 明示的な文字コード設定は不要

3. **データ型の互換性**
   - ほとんどのDjangoフィールドは自動的に変換されます
   - カスタムSQLを使用している場合は確認が必要

## 移行完了日

2026年1月3日

## 作成者

AI Assistant (Claude Sonnet 4.5)

