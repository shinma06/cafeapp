# Cafe-App

## 概要

Cafe-Appは、架空のカフェのウェブアプリケーションです。DjangoとMySQLを使用し、Dockerを利用して環境を構築しました。このプロジェクトは、学習目的で作成しました。

## 機能説明

Cafe-Appでは、従業員側とユーザー側の機能が分けられています。

### 従業員側の機能

- **メニュー管理**: 従業員はメニュー項目の追加、編集、削除が可能です。
- **予約管理**: カフェの予約状況を確認することができます。
- **ニュース投稿**: カフェのニュースやイベント情報を投稿、編集、削除できます。
- **お問い合わせ対応**: ユーザーからのお問い合わせメールを受信し、管理できます。

### ユーザー側の機能

- **メニュー閲覧**: カフェのメニューを閲覧できます。
- **オンライン予約**: カフェのテーブルをオンラインで予約できます。
- **ニュース閲覧**: カフェの最新ニュースをカテゴリごとに絞り込んで確認できます。
- **お問い合わせ**: カフェへのお問い合わせをメールで送信できます。
- **アカウント**: アカウントの作成、ログイン、ログアウト、ユーザー名の変更ができます。

※リポジトリからインストールして使用する場合メール機能は使用できません。

## 技術スタック

- **Python**: 3.12
- **Django**: 5.1+
- **MySQL**: 8.0
- **Docker Compose**: 最新版
- **Tailwind CSS**: 3.4+
- **Node.js**: 20 (Tailwindビルド用)
- **その他のライブラリ**: requirements.txtを参照

## システム要件

- Docker Desktop（最新版を推奨）
- Git

## インストール方法

1. リポジトリをクローン

```bash
git clone https://github.com/shinma06/cafe-app
cd cafe-app
```

2. 環境変数の設定

```bash
cp env.sample .env
# .envファイルを編集して必要な設定を行ってください
```

3. Dockerコンテナのビルドと起動

```bash
docker compose build
docker compose up -d
```

4. データベースのマイグレーション（初回のみ）

```bash
docker compose exec web python manage.py migrate
```

5. 静的ファイルの収集（必要に応じて）

```bash
docker compose exec web python manage.py collectstatic --noinput
```

## 使用方法

アプリケーションは http://localhost:8000 でアクセス可能です。

## 管理者アカウントの作成

1. 稼働中のコンテナを確認

まずは`docker ps`コマンドを使って、現在稼働中のコンテナの状態を確認します。

```bash
docker ps
```

出力例：

```
CONTAINER ID   IMAGE         COMMAND                   CREATED      STATUS          PORTS                               NAMES
xxxxxxxxxxxx   cafe-app-web   "./combined_script.sh"    x days ago   Up x minutes   0.0.0.0:8000->8000/tcp              cafe-app-web
xxxxxxxxxxxx   mysql:8.0     "docker-entrypoint.s…"   x days ago   Up x minutes   0.0.0.0:3306->3306/tcp, 33060/tcp   cafe-app-mysql
```

2. Djangoのスーパーユーザーを作成

Cafe-Appのコンテナ内でDjangoのスーパーユーザーを作成するために、以下のコマンドを実行します。ここで`xxx`は`docker ps`コマンドの出力で表示されたcafe-app-webコンテナのCONTAINER IDの頭文字2～3文字に置き換えてください。

```bash
docker exec -it xxx bash
```

次に、Djangoのスーパーユーザーを作成します。

```bash
python manage.py createsuperuser
```

以下の手順でユーザー情報を入力します：

- **ユーザー名**：任意のユーザー名を入力して Enter
- **メールアドレス**：何も入力せず Enter
- **パスワード**：任意のパスワードを入力して Enter（簡単なもので構いません）
- **パスワード（再入力）**：先ほど入力したパスワードを再度入力して Enter

パスワードの複雑性に関する警告が表示される場合：`y`を入力して Enter。これでスーパーユーザーが作成されます。

成功すると、「Superuser created successfully.」と表示されます。

作成したユーザー名とパスワードでログインすることで従業員用の機能が使用できるようになります。

## 開発コマンド

### コンテナの起動・停止

```bash
# バックグラウンドで起動
docker compose up -d

# フォアグラウンドで起動（ログを確認）
docker compose up

# 停止
docker compose stop

# 停止して削除
docker compose down

# ボリュームも含めて完全削除
docker compose down -v
```

### ログの確認

```bash
# すべてのログ
docker compose logs

# 特定のサービスのログ
docker compose logs web
docker compose logs mysql

# リアルタイムでログを追跡
docker compose logs -f web
```

### コンテナ内でのコマンド実行

```bash
# Djangoシェル
docker compose exec web python manage.py shell

# データベースのマイグレーション
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# テストの実行
docker compose exec web python manage.py test

# Tailwind CSSのビルド
make tailwind-build

# Tailwind CSSのwatchモード（開発時）
make tailwind-watch
```

## プロジェクト構造

```
cafe-app/
├── accounts/           # ユーザー認証アプリ
├── pages/              # メインアプリ（メニュー、ニュース、予約等）
├── cafe-app/            # プロジェクト設定
├── templates/          # テンプレートファイル
├── static/             # 静的ファイル
│   ├── src/            # Tailwind CSSソース
│   └── dist/           # Tailwind CSSビルド出力
├── media/              # アップロードされたメディアファイル
├── docker/             # Docker関連設定
│   └── mysql/
│       └── conf.d/     # MySQL設定ファイル
├── Dockerfile          # Djangoイメージ定義
├── Dockerfile.node     # Node.js/Tailwindイメージ定義
├── docker-compose.yml  # Docker Compose設定
├── requirements.txt    # Pythonパッケージ
├── package.json        # Node.jsパッケージ
├── tailwind.config.js  # Tailwind CSS設定
├── env.sample          # 環境変数サンプル
└── README.md           # このファイル
```

## 環境変数

プロジェクトで使用する主な環境変数は`env.sample`を参照してください。本番環境では必ず以下の設定を変更してください：

- `DJANGO_SECRET_KEY`: 秘密鍵（ランダムな文字列）
- `DJANGO_DEBUG`: False に設定
- `DJANGO_ALLOWED_HOSTS`: 実際のホスト名に設定
- `MYSQL_PASSWORD`、`MYSQL_ROOT_PASSWORD`: 強力なパスワードに変更

## トラブルシューティング

### データベース接続エラー

MySQLコンテナが完全に起動するまで待つ必要があります。`docker compose logs mysql`でログを確認してください。

### ポートが既に使用されている

ポート8000や3306が既に使用されている場合は、`.env`ファイルで`WEB_PORT`や`MYSQL_PORT`を変更してください。

### 静的ファイルが読み込まれない

```bash
docker compose exec web python manage.py collectstatic --noinput
```

## セキュリティに関する注意

- 本番環境では`DEBUG = False`に設定してください
- `.env`ファイルはGitにコミットしないでください
- 強力なパスワードを使用してください
- 定期的に依存パッケージを更新してください

## 参考文献・ウェブサイト

### 書籍

[1冊ですべて身につくHTML & CSSとWebデザイン入門講座](https://www.sbcr.jp/product/4797398892/)
この書籍は、HTMLとCSSに関する基本的な概念と実践的なコーディング技術を紹介しています。

### ウェブサイト

[ページネーションデザイン](https://eclair.blog/example-of-pagination/)
このサイトは、コピペですぐに導入できるシンプルで汎用的なページネーションデザインのアイデアを提供しています。

## 開発の動機と学び

このプロジェクトを通じて、Djangoの基本、データベースとの連携、Dockerを使用した環境構築などのスキルを学習しました。

## ライセンス

このプロジェクトは学習目的で作成されています。

## 作成者

shinma06

## 現在のステータス

基本機能は実装済みです。メニュー詳細ページの追加など、さらなる機能拡張を検討中です。
