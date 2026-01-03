# データベーストラブルシューティングガイド

## 問題: マイグレーションエラー「Table already exists」

### 原因
古いデータベースデータがボリュームに残っているため、新しいマイグレーションが失敗します。

### 完全な解決手順

```bash
# 1. すべてのコンテナとボリュームを停止・削除
docker compose down -v

# 2. ボリュームが確実に削除されたか確認
docker volume ls | grep cafe-app

# 3. 残っている場合は手動で削除
docker volume rm cafe-app_mysql_data
docker volume rm cafe-app_static_volume
docker volume rm cafe-app_media_volume

# 4. dataディレクトリがあれば削除（以前の設定で使用されていた場合）
rm -rf data/

# 5. 再セットアップ
make setup

# または
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate
```

### 予防策

```bash
# 開発中にデータをリセットしたい場合
make clean    # ボリュームも含めて削除
make setup    # 再構築

# または
make rebuild  # clean + setup を一度に実行
```

## 問題: MySQLの起動が遅い

### 原因
1. ヘルスチェックの設定
2. MySQLの初期化プロセス
3. システムリソース

### 最適化済みの設定

**docker-compose.yml:**
```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD:-0103}"]
  interval: 5s      # チェック間隔（短くして早期検知）
  timeout: 3s       # タイムアウト
  retries: 10       # リトライ回数
  start_period: 20s # 初回起動の猶予期間
```

### 起動時間の目安
- 初回起動: 15-20秒
- 2回目以降: 5-10秒（ボリュームにデータが残っている場合）

### 確認コマンド

```bash
# MySQLコンテナのログを確認
docker compose logs mysql

# ヘルスチェックの状態を確認
docker compose ps

# リアルタイムで起動を監視
docker compose logs -f mysql
```

## 問題: Tailwindコンテナが起動しない

### 確認

```bash
# すべてのコンテナを確認
docker compose ps

# Tailwindコンテナのログを確認
docker compose logs tailwind
```

### 起動していない場合

```bash
# 手動で起動
docker compose up -d tailwind

# または全体を再起動
docker compose restart
```

## 完全なクリーンアップスクリプト

開発中に完全にリセットしたい場合：

```bash
#!/bin/bash
# cleanup.sh

echo "🧹 完全クリーンアップを開始します..."

# コンテナとボリュームを削除
docker compose down -v

# Dockerボリュームを確認して削除
echo "📦 ボリュームを削除中..."
docker volume rm cafe-app_mysql_data 2>/dev/null || true
docker volume rm cafe-app_static_volume 2>/dev/null || true
docker volume rm cafe-app_media_volume 2>/dev/null || true

# dataディレクトリがあれば削除
if [ -d "data" ]; then
    echo "📁 dataディレクトリを削除中..."
    rm -rf data/
fi

# 未使用のボリュームをクリーンアップ
docker volume prune -f

echo "✅ クリーンアップ完了！"
echo ""
echo "次のステップ:"
echo "  make setup"
```

使用方法:
```bash
chmod +x cleanup.sh
./cleanup.sh
make setup
```

## Makefileのヘルパーコマンド

既に実装済み：

```bash
make clean      # コンテナとボリュームを削除
make clean-all  # イメージも含めて完全削除
make rebuild    # clean + setup を実行
```

## データベースのバックアップ（重要なデータがある場合）

```bash
# バックアップ
docker exec cafe-app-mysql mysqldump -u root -p0103 cafe-app > backup_$(date +%Y%m%d).sql

# リストア
docker exec -i cafe-app-mysql mysql -u root -p0103 cafe-app < backup_YYYYMMDD.sql
```

## トラブルシューティングチェックリスト

データベース問題が発生したら：

- [ ] `docker compose down -v`を実行した
- [ ] `docker volume ls`でボリュームが削除されたか確認
- [ ] `data/`ディレクトリが存在しないか確認
- [ ] 再ビルド: `docker compose build --no-cache`
- [ ] 起動: `docker compose up -d`
- [ ] MySQLのヘルスチェックを確認: `docker compose ps`
- [ ] マイグレーション: `make migrate`

それでも解決しない場合：

```bash
# 完全リセット
docker compose down -v
docker volume prune -f
docker system prune -f
make setup
```

