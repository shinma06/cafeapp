# ネーミング統一完了ドキュメント

## 概要

プロジェクト全体のネーミングを **`cafe-app`** に統一しました。

## 統一前の状態

プロジェクト内に複数のネーミングが混在していました：

- `cafeapp`
- `CafeApp`
- `WCB Cafe`
- `WCB CAFE`
- `WEBカフェ`
- `Webカフェ`

## 統一後のネーミング

すべて **`Cafe-App`** または **`cafe-app`** に統一しました。

### 使い分け

- **表示名**: `Cafe-App` （ハイフン付き、大文字）
- **技術名**: `cafe-app` または `cafe_app` （ハイフン付き、小文字）
  - Docker: `cafe-app-*`
  - データベース: `cafe_app` （PostgreSQLの命名規則に従う）
  - Python変数: 既存の`cafeapp`は維持（Djangoプロジェクト名）

## 変更されたファイル

### 1. Docker関連

#### **docker-compose.yml**
```yaml
# コンテナ名
container_name: cafe-app-postgres
container_name: cafe-app-web

# データベース名
POSTGRES_DB: cafe_app

# DATABASE_URL
DATABASE_URL: postgres://shinma:0103@postgres:5432/cafe_app

# ワーキングディレクトリ
volumes:
  - .:/app
```

#### **Dockerfile**
```dockerfile
WORKDIR /app
```

### 2. Makefile

```makefile
help:
	@echo "Cafe App 開発コマンド"

dbshell:
	docker compose exec postgres psql -U shinma -d cafe_app

tailwind:
	docker build -f Dockerfile.node -t cafe-app-tailwind .
	docker run --rm -v $(PWD)/static:/app/static cafe-app-tailwind npm run build:css
```

### 3. テンプレート

すべてのHTMLテンプレートで以下を置換：

- `WCB Cafe` → `Cafe-App`
- `WCB CAFE` → `Cafe-App`
- `WEBカフェ` → `Cafe-App`
- `Webカフェ` → `Cafe-App`

#### **base.html**
```html
<title>{% block title %}Cafe-App{% endblock title %}</title>
<a href="{% url 'pages:index' %}" aria-label="Cafe-App ホーム">
  <img src="..." alt="Cafe-App ロゴ">
</a>
```

#### **各ページテンプレート**
```html
{% block title %}Cafe-App - NEWS{% endblock title %}
{% block title %}Cafe-App - MENU{% endblock title %}
{% block title %}Cafe-App - BOOKING{% endblock title %}
{% block title %}Cafe-App - CONTACT{% endblock title %}
```

### 4. package.json

```json
{
    "name": "cafe-app",
    "version": "1.0.0",
    "description": "Cafe-App with Tailwind CSS"
}
```

### 5. ドキュメント

すべてのMarkdownファイル（*.md）で以下を置換：

- `cafeapp` → `cafe-app`
- `CafeApp` → `Cafe-App`
- `WCB Cafe` → `Cafe-App`
- `WCB CAFE` → `Cafe-App`

対象ファイル：
- README.md
- POSTGRESQL_MIGRATION.md
- SIMPLIFICATION.md
- TAILWIND_MIGRATION.md
- DATABASE_TROUBLESHOOTING.md
- MIGRATION_GUIDE.md
- REFACTORING_SUMMARY.md
- CHANGELOG.md
- SETUP_COMPLETE.md
- その他すべてのドキュメント

## 変更されなかったもの

以下は既存の構造を維持するため、変更していません：

### Djangoプロジェクト名
```
cafeapp/  # ディレクトリ名
├── cafeapp/  # Djangoプロジェクト設定ディレクトリ
│   ├── settings.py
│   ├── urls.py
│   └── ...
```

**理由**: Djangoプロジェクトの構造を変更すると、多くのインポートパスやURLパターンを修正する必要があり、リスクが高いため。

### Djangoアプリ名
```
pages/
accounts/
```

**理由**: アプリ名の変更はマイグレーションに影響するため。

### 環境変数・設定
```python
# settings.py
DJANGO_SETTINGS_MODULE = cafeapp.settings  # 維持
```

## 新しいコンテナ名

```bash
$ docker compose ps
NAME                STATUS
cafe-app-postgres   Up (healthy)
cafe-app-web        Up
```

## データベース名

```bash
# PostgreSQL接続
$ make dbshell
psql (16.11)
Type "help" for help.

cafe_app=>
```

## 確認方法

### 1. コンテナ名の確認
```bash
docker compose ps
```

期待される出力：
```
NAME                IMAGE                COMMAND
cafe-app-postgres   postgres:16-alpine   ...
cafe-app-web        cafeapp-web          ...
```

### 2. ページタイトルの確認
```bash
curl -s http://localhost:8000 | grep "<title>"
```

期待される出力：
```html
<title>Cafe-App</title>
```

### 3. データベース名の確認
```bash
make dbshell
\l  # データベース一覧
```

期待される出力：
```
cafe_app | shinma | UTF8 | ...
```

## 移行手順

既存環境から新しいネーミングに移行する場合：

```bash
# 1. 完全クリーンアップ
make clean

# 2. 新しい環境でセットアップ
make setup

# 3. スーパーユーザー作成
make createsuperuser
```

## 注意事項

### データベース名の変更

データベース名が `cafeapp` から `cafe_app` に変更されています。

既存のデータを移行する場合：

```bash
# 旧環境でデータをエクスポート
docker compose exec web python manage.py dumpdata > data.json

# 新環境でインポート
docker compose exec web python manage.py loaddata data.json
```

### Docker イメージ名

Dockerイメージ名は自動生成されるため、`cafeapp-web`のままです。
これは問題ありません（内部的な名前のため）。

## 一貫性のあるネーミング規則

今後の開発では以下の規則に従ってください：

### 表示名（ユーザーに見える部分）
- **`Cafe-App`** （ハイフン付き、大文字始まり）
- 例: ページタイトル、ロゴのalt属性、ドキュメント

### 技術名（システム内部）
- **`cafe-app`** （ハイフン付き、小文字）
- 例: Dockerコンテナ名、package.json

- **`cafe_app`** （アンダースコア、小文字）
- 例: データベース名、PostgreSQLテーブル名

### Djangoプロジェクト名（既存維持）
- **`cafeapp`** （ハイフンなし、小文字）
- 例: settings.py、urls.py、インポートパス

## 統一完了日

2026年1月3日

## 作成者

AI Assistant (Claude Sonnet 4.5)

---

**結論**: プロジェクト全体のネーミングが `Cafe-App` / `cafe-app` に統一され、一貫性が向上しました！🎉

