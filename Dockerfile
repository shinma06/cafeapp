# マルチステージビルドを使用して最適化
FROM python:3.12-slim as base

# Pythonの出力バッファリングを無効化
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 作業ディレクトリの設定
WORKDIR /cafeapp

# 依存関係のインストール（キャッシュ最適化のため分離）
FROM base as dependencies

# システムパッケージの更新とMySQL、netcatクライアントのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージのインストール
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# 最終ステージ
FROM base as final

# システムパッケージのインストール（実行時に必要なもののみ）
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 依存関係ステージからPythonパッケージをコピー
COPY --from=dependencies /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# 非rootユーザーの作成
RUN useradd -m -u 1000 cafeapp && \
    chown -R cafeapp:cafeapp /cafeapp

# アプリケーションファイルのコピー
COPY --chown=cafeapp:cafeapp . .

# 起動スクリプトに実行権限を付与
RUN chmod +x combined_script.sh

# 非rootユーザーに切り替え
USER cafeapp

# ポート8000を公開
EXPOSE 8000

# デフォルトコマンド
CMD ["./combined_script.sh"]
