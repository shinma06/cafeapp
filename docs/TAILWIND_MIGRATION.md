# Tailwind CSS 移行完了ドキュメント

## 概要

このプロジェクトのすべてのCSSをTailwind CSSに移行しました。古い `style.css` ファイルは削除され、すべてのスタイリングはTailwind CSSを使用して実装されています。

## 移行したページ一覧

### Pages アプリ

1. **ホームページ** (`index.html`)
   - 中央配置のヒーローセクション
   - カスタムボタンスタイル

2. **ニュース関連**
   - `news.html` - ニュース一覧（グリッドレイアウト、サイドバー）
   - `news_create.html` - ニュース作成フォーム

3. **メニュー関連**
   - `menu.html` - メニュー一覧（グリッドレイアウト、カード）
   - `menu_detail.html` - メニュー詳細
   - `menu_create.html` - メニュー作成フォーム
   - `menu_posted.html` - メニュー投稿完了

4. **予約関連**
   - `booking.html` - 予約フォーム
   - `booking_confirm.html` - 予約確認
   - `booking_complete.html` - 予約完了
   - `booking_list.html` - 予約一覧（管理者向け）

5. **お問い合わせ**
   - `contact.html` - お問い合わせフォーム、地図、SNS埋め込み

### Accounts アプリ

1. **認証関連**
   - `login.html` - ログインフォーム
   - `login_complete.html` - ログイン完了
   - `signup.html` - 新規登録フォーム
   - `signup_complete.html` - 新規登録完了
   - `logout_complete.html` - ログアウト完了

2. **アカウント管理**
   - `account_edit.html` - アカウント編集（モーダル付き）
   - `rename_complete.html` - ユーザー名変更完了

## カスタムテーマ

`tailwind.config.js` で以下のカスタムカラーとフォントを定義：

### カラー
- `cafe-brown`: `#432` - メインのブラウン
- `cafe-cyan`: `#0bd` - アクセントカラー
- `cafe-cyan-dark`: `#099` - 濃いめのシアン
- `cafe-bg`: `#e6e6e6` - 背景色

### フォント
- `philosopher`: Philosopher（ページタイトル用）
- `yugothic`: Yu Gothic Medium（本文用）

## カスタムコンポーネント

`static/src/input.css` で以下のカスタムコンポーネントを定義：

### ボタン
```css
.btn-primary
```
- カフェテーマのプライマリボタン
- ホバー効果、トランジション付き

### ページタイトル
```css
.page-title-custom
```
- 大きなページタイトルスタイル
- Philosopherフォント使用

### 背景画像
各ページIDに対応する背景画像を定義：
- `#home` - メインの背景
- `#complete` - 完了ページの背景
- `#news` - ニュースページの背景
- `#menu` - メニューページの背景
- `#contact`, `#accounts` - コンタクト/アカウントページの背景
- `#menu-detail` - メニュー詳細の背景

## フォームスタイリング

すべてのフォームに一貫したスタイルを適用：
- ラベル: 太字、ブラウンカラー
- 入力フィールド: ボーダー、フォーカス時のリング効果
- テキストエリア: 最小高さ150px
- ボタン: カスタムボタンスタイル

## レスポンシブデザイン

Tailwindのレスポンシブユーティリティを使用：
- モバイルファースト
- `md:` ブレークポイント（768px以上）
- `lg:` ブレークポイント（1024px以上）

## ビルドプロセス

### ビルド
```bash
make tailwind
```

このコマンドは以下を実行します：
1. `Dockerfile.node`からTailwind用のDockerイメージをビルド
2. コンテナを実行してTailwind CSSをビルド
3. ビルドされたCSSを`static/dist/output.css`に出力

### 出力ファイル
- 入力: `static/src/input.css`
- 出力: `static/dist/output.css`

## 削除されたファイル

以下のファイルは不要になったため削除されました：
- `static/pages/css/style.css` - 古いカスタムCSSファイル

## 注意事項

1. **Admin CSSは残されています**
   - Django管理画面のCSSファイルは保持
   - `static/admin/css/` 配下のファイルは削除されていません

2. **jQuery UI CSS**
   - 予約ページのDatepicker用にCDNから読み込み
   - 将来的にはTailwindベースのDatepickerへの移行を検討

3. **外部埋め込み**
   - SNS埋め込み（Facebook、Twitter、YouTube）のスタイルは変更なし
   - Google Mapsの埋め込みも維持

## 今後の改善案

1. **CSS in HTML**
   - フォームスタイルがHTML内の`<style>`タグに含まれている
   - 将来的には完全にTailwindクラスのみで実装することを検討

2. **コンポーネント化**
   - 共通のカードやモーダルをコンポーネント化
   - 再利用性の向上

3. **ダークモード**
   - Tailwindのダークモード機能を活用
   - カフェテーマに合わせたダークモード実装

## 完了日

2026年1月3日

## 作成者

AI Assistant (Claude Sonnet 4.5)
