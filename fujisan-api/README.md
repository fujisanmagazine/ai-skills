# Fujisan API スキル

Fujisan API の公式ドキュメントを参照するためのエージェントスキルです。`https://apidoc.fujisan.co.jp/` のドキュメントのみを読み取り、業務用の Fujisan API は呼び出しません。

## インストール

[skills CLI](https://github.com/vercel-labs/skills) を使って GitHub からインストールします。現在の CLI には Node.js 22.20.0 以降が必要です。インストールするユーザーには、非公開リポジトリ `fujisanmagazine/ai-skills` への読み取り権限が必要です。自分の端末で次のコマンドを実行し、認証とアクセス権を確認してください。

```sh
gh auth login -h github.com --git-protocol https --web
gh auth status
gh repo view fujisanmagazine/ai-skills
```

すでにログイン済みの場合は、`gh auth login` を省略できます。組織で SAML SSO が必要な場合は、必要に応じて [GitHub CLI のアプリに組織へのアクセスを許可](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-single-sign-on/authorizing-an-app-for-single-sign-on)してください。その後、スキルを使いたいプロジェクトで次のコマンドを実行します。

```sh
npx skills add fujisanmagazine/ai-skills --skill fujisan-api -a cursor -y && printf '%s\n' \
  'fujisan-api の認証設定:' \
  '1. ~/.config/fujisan/apidoc.env を作成し、APIDOC_BASIC_USERNAME と APIDOC_BASIC_PASSWORD を設定してください。' \
  '2. 自分だけが読み書きできるようにしてください: chmod 600 ~/.config/fujisan/apidoc.env' \
  '3. 認証情報を読み込むラッパースクリプトと使い方は、インストールしたスキルの README を参照してください。'
```

Node.js 20 を使用している端末では、互換性のある Node.js を一時的に使って CLI を実行します。

```sh
npx --yes --package=node@22.20.0 --package=skills -- skills add fujisanmagazine/ai-skills --skill fujisan-api -a cursor -y && printf '%s\n' \
  'fujisan-api の認証設定:' \
  '1. ~/.config/fujisan/apidoc.env を作成し、APIDOC_BASIC_USERNAME と APIDOC_BASIC_PASSWORD を設定してください。' \
  '2. 自分だけが読み書きできるようにしてください: chmod 600 ~/.config/fujisan/apidoc.env' \
  '3. 認証情報を読み込むラッパースクリプトと使い方は、インストールしたスキルの README を参照してください。'
```

Codex で使う場合は `-a codex`、Claude Code で使う場合は `-a claude-code` に変更してください。`-g` を追加すると、現在のプロジェクトではなくグローバルにインストールできます。CLI は、既存の Git 認証情報ヘルパーや、アクセスを許可された SSH キーも利用できます。リポジトリを手動でクローンしたり、npm パッケージとして公開したりする必要はありません。

## ドキュメント取得時の認証設定

ドキュメントサーバーは Basic 認証を使用します。エージェントを実行する環境に `APIDOC_BASIC_USERNAME` と `APIDOC_BASIC_PASSWORD` を設定してください。認証情報をプロジェクト内のファイルやエージェントの設定ファイルに保存しないでください。

ドキュメント用の認証情報は、リポジトリの外にある `~/.config/fujisan/apidoc.env` に保存し、自分だけが読み取れるようにします。エディターで開く前に、次のコマンドでファイルを作成してアクセス権を制限してください。

```sh
mkdir -p ~/.config/fujisan
touch ~/.config/fujisan/apidoc.env
chmod 600 ~/.config/fujisan/apidoc.env
${EDITOR:-vi} ~/.config/fujisan/apidoc.env
```

ファイルに `APIDOC_BASIC_USERNAME=...` と `APIDOC_BASIC_PASSWORD=...` を、それぞれ別の行にシェルの変数代入形式で記述します。ドキュメントサーバー用に発行された認証情報を使用してください。認証情報をチャットやシェルコマンドに貼り付けないでください。

スキルには `scripts/with-apidoc-creds.sh` が付属しています。このラッパースクリプトは認証情報ファイルを読み込み、認証情報を環境変数に設定してコマンドを実行します。認証情報はコマンドライン引数、シェル履歴、スクリプトの出力には含まれません。ファイルを所有者以外が読み取れる場合、ラッパースクリプトは実行を拒否します。別のパスを使う場合は `APIDOC_ENV_FILE` を設定してください。

スキルのディレクトリで、次のコマンドを実行します。

```sh
scripts/with-apidoc-creds.sh python3 scripts/fetch_apidoc.py /api-index.json
```

## ローカルでの検証

```sh
python3 -m unittest discover -s test
```
