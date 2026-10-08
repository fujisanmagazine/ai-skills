# Fujisan OpenSearch 読み取り専用ログ調査スキル

この Agent Skill は、Fujisan の OpenSearch クラスターにあるサーバー・アプリケーションログ、Webアクセスログ、Windowsイベントを読み取り専用で調査するためのスキルです。利用時には、ワークスペースの `.env` ファイルに `OPENSEARCH_USER` と `OPENSEARCH_PASSWORD` を設定する必要があります。

## 調査対象

| インデックスパターン | 用途 |
|---|---|
| `collect-logs-*` | すべてのサーバーのログを集約 |
| `pound-logs-*` | Pound・ELB・API GatewayのWebアクセスログ |
| `windows-event-logs-*` | Windowsイベントログ |

調査時は期間と対象ホスト・サービスなどを指定してください。ホストを `z86` に固定する制約はありません。タイムゾーンの指定がない場合は日本時間（Asia/Tokyo）で解釈します。

例: 「opensearch で、2026年10月8日15時から16時（JST）の zasshi-catalog1 の nginx/catalog-page-admin ログを調べてください。」

フィールドの説明とログ種別ごとの注意点は [ログスキーマ資料](references/log-schema.md) を参照してください。資料は提供されたサンプルに基づき、マッピングや全ログでのフィールド存在を保証するものではありません。

## インストール

[skills CLI](https://github.com/vercel-labs/skills) を使ってリポジトリからインストールできます。現在の CLI には Node.js 22.20.0 以降が必要です。インストールするユーザーには、非公開リポジトリ `fujisanmagazine/ai-skills` への読み取り権限が必要です。各自の端末で、次のコマンドを使って認証とアクセス権を確認してください。

```sh
gh auth login -h github.com --git-protocol https --web
gh auth status
gh repo view fujisanmagazine/ai-skills
```

すでにログイン済みの場合は、`gh auth login` を省略できます。組織で SAML SSO が必須の場合は、必要に応じて [GitHub CLI のアプリに組織へのアクセスを承認](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-single-sign-on/authorizing-an-app-for-single-sign-on)してください。その後、スキルを利用したいプロジェクトで次のコマンドを実行します。

```sh
npx skills add fujisanmagazine/ai-skills --skill opensearch -a cursor -y && printf '%s\n' \
  'opensearch の認証設定:' \
  '1. ワークスペースの .env ファイルに OPENSEARCH_USER と OPENSEARCH_PASSWORD を追加してください。' \
  '2. .env を Git の管理対象から除外し、アクセス権を制限してください: chmod 600 .env' \
  '3. 詳しい設定手順は、インストールしたスキルの README を参照してください。'
```

Node.js 20 を使用している端末では、一時的に対応バージョンの Node.js を使って CLI を実行します。

```sh
npx --yes --package=node@22.20.0 --package=skills -- skills add fujisanmagazine/ai-skills --skill opensearch -a cursor -y && printf '%s\n' \
  'opensearch の認証設定:' \
  '1. ワークスペースの .env ファイルに OPENSEARCH_USER と OPENSEARCH_PASSWORD を追加してください。' \
  '2. .env を Git の管理対象から除外し、アクセス権を制限してください: chmod 600 .env' \
  '3. 詳しい設定手順は、インストールしたスキルの README を参照してください。'
```

Codex を利用する場合は `-a codex`、Claude Code を利用する場合は `-a claude-code` を指定してください。現在のプロジェクトではなくグローバルにインストールするには、`-g` を追加します。CLI は、既存の Git 認証ヘルパーや、アクセス権のある SSH キーも利用できます。

リポジトリのクローンや npm パッケージの公開は不要です。

## OpenSearch への接続に必要な認証情報

OpenSearch クラスターへの接続にはアカウントが必要です。スキルを実行するワークスペースで `.env` ファイルを作成し、アクセス権を制限してから編集してください。

```sh
touch .env
chmod 600 .env
${EDITOR:-vi} .env
```

`OPENSEARCH_USER=...` と `OPENSEARCH_PASSWORD=...` を、それぞれ別の行にシェルの変数代入形式で記述してください。OpenSearch クラスター用に発行された認証情報を使用します。`.env` は Git の管理対象から除外してください（`git check-ignore .env` の出力にファイルが表示されることを確認します）。認証情報をチャットやシェルコマンドに貼り付けないでください。スキルは実行時にこのファイルを読み込みます。
