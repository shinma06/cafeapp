# ネーミング統一完了ドキュメント

## 概要

プロジェクト全体のネーミングを **`cafeapp`** に統一しました。

## 統一前の状態

プロジェクト内に複数のネーミングが混在していました：

- `cafe-app`（ハイフン付き - Pythonで使用不可）
- `Cafe-App`（ハイフン付き）
- `cafe_app`（アンダースコア）
- `WCB Cafe`
- `WCB CAFE`
- `WEBカフェ`
- `Webカフェ`

## 統一後のネーミング

すべて **`CafeApp`** または **`cafeapp`** に統一しました。

### 使い分け

- **表示名**: `CafeApp` （ハイフンなし、大文字始まり）
- **技術名**: `cafeapp` （ハイフンなし、小文字）
  - Docker: `cafeapp-*`
  - データベース: `cafeapp`
  - Python変数: `cafeapp`（Djangoプロジェクト名）

## 変更されたファイル

### 1. Pythonファイル

#### **cafeapp/settings.py**
```python
INSTALLED_APPS = [
    'cafeapp',
    'pages.apps.PagesConfig',
    ...
]

ROOT_URLCONF = 'cafeapp.urls'
WSGI_APPLICATION = 'cafeapp.wsgi.application'
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://shinma:0103@postgres:5432/cafeapp')
```

#### **cafeapp/asgi.py**
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafeapp.settings')
```

#### **cafeapp/wsgi.py**
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafeapp.settings')
```

#### **cafeapp/urls.py**
```python
# URL configuration for cafeapp project.
```

#### **cafeapp/management/commands/runcontainer.py**
```python
non_default_apps = [app for app in installed_apps if not app.name.startswith('django.contrib.') and app.name != 'cafeapp']
```

### 2. Docker関連

#### **docker-compose.yml**
```yaml
# コンテナ名
container_name: cafeapp-postgres
container_name: cafeapp-web

# データベース名
POSTGRES_DB: cafeapp

# DATABASE_URL
DATABASE_URL: postgres://shinma:0103@postgres:5432/cafeapp

# ワーキングディレクトリ
volumes:
  - .:/app
```

#### **Dockerfile.node**
```dockerfile
COPY ./cafeapp ./cafeapp
```

### 3. Makefile

```makefile
help:
	@echo "CafeApp 開発コマンド"

dbshell:
	docker compose exec postgres psql -U shinma -d cafeapp

tailwind:
	docker build -f Dockerfile.node -t cafeapp-tailwind .
	docker run --rm -v $(PWD)/static:/app/static cafeapp-tailwind npm run build:css
```

### 4. package.json

```json
{
    "name": "cafeapp",
    "version": "1.0.0",
    "description": "CafeApp with Tailwind CSS"
}
```

### 5. tailwind.config.js

```javascript
content: [
    './cafeapp/**/*.py',
    ...
]
```

### 6. テンプレート

すべてのHTMLテンプレートで以下を置換：

- `WCB Cafe` → `CafeApp`
- `WCB CAFE` → `CafeApp`
- `WEBカフェ` → `CafeApp`
- `Webカフェ` → `CafeApp`
- `Cafe-App` → `CafeApp`

#### **base.html**
```html
<title>{% block title %}CafeApp{% endblock title %}</title>
<a href="{% url 'pages:index' %}" aria-label="CafeApp ホーム">
  <img src="..." alt="CafeApp ロゴ">
</a>
```

#### **各ページテンプレート**
```html
{% block title %}CafeApp - NEWS{% endblock title %}
{% block title %}CafeApp - MENU{% endblock title %}
{% block title %}CafeApp - BOOKING{% endblock title %}
{% block title %}CafeApp - CONTACT{% endblock title %}
```

### 7. ドキュメント

すべてのMarkdownファイル（*.md）で以下を置換：

- `cafe-app` → `cafeapp`
- `Cafe-App` → `CafeApp`
- `cafe_app` → `cafeapp`（データベース名も統一）
- `WCB Cafe` → `CafeApp`
- `WCB CAFE` → `CafeApp`

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
my-cafe-app/  # ディレクトリ名
├── cafeapp/  # Djangoプロジェクト設定ディレクトリ
│   ├── settings.py
│   ├── urls.py
│   └── ...
```

**理由**: Djangoプロジェクトの構造は既に`cafeapp`で統一されているため、変更不要。

### Djangoアプリ名
```
pages/
accounts/
```

**理由**: アプリ名の変更はマイグレーションに影響するため。

## 新しいコンテナ名

```bash
$ docker compose ps
NAME                STATUS
cafeapp-postgres    Up (healthy)
cafeapp-web         Up
```

## データベース名

```bash
# PostgreSQL接続
$ make dbshell
psql (16.11)
Type "help" for help.

cafeapp=>
```

## 確認方法

### 1. コンテナ名の確認
```bash
docker compose ps
```

期待される出力：
```
NAME                IMAGE                COMMAND
cafeapp-postgres    postgres:16-alpine   ...
cafeapp-web         cafeapp-web          ...
```

### 2. ページタイトルの確認
```bash
curl -s http://localhost:8000 | grep "<title>"
```

期待される出力：
```html
<title>CafeApp</title>
```

### 3. データベース名の確認
```bash
make dbshell
\l  # データベース一覧
```

期待される出力：
```
cafeapp | shinma | UTF8 | ...
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

データベース名が `cafe_app` から `cafeapp` に変更されています。

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
- **`CafeApp`** （ハイフンなし、大文字始まり）
- 例: ページタイトル、ロゴのalt属性、ドキュメント

### 技術名（システム内部）
- **`cafeapp`** （ハイフンなし、小文字）
- 例: Dockerコンテナ名、package.json、データベース名、Python変数、Djangoプロジェクト名

### 重要なポイント

- **Pythonファイルではハイフン（`-`）は使用不可**のため、すべて`cafeapp`（ハイフンなし）に統一
- データベース名も`cafeapp`に統一（PostgreSQLではハイフンは使用可能だが、一貫性のため統一）
- 表示名は`CafeApp`（ハイフンなし、大文字始まり）で統一

## 統一完了日

2026年1月3日（修正版）

## 作成者

AI Assistant (Claude Sonnet 4.5)

---

**結論**: プロジェクト全体のネーミングが `CafeApp` / `cafeapp` に統一され、Pythonファイルでのエラーが解消されました！🎉
