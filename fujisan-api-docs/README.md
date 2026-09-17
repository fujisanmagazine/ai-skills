# Fujisan API Docs Skill

An Agent Skill for consulting the primary Fujisan API documentation. It reads only documentation resources from `https://apidoc.fujisan.co.jp/`; it does not call operational Fujisan APIs.

The documentation server uses Basic authentication. Set `APIDOC_BASIC_USERNAME` and `APIDOC_BASIC_PASSWORD` in the environment that runs the agent. Do not store them in project files or agent configuration.

## Install

After publishing this package to your npm registry, install the skill with `npx`:

```sh
npx @fujisan/skill-fujisan-api-docs --target codex
npx @fujisan/skill-fujisan-api-docs --target claude
npx @fujisan/skill-fujisan-api-docs --target cursor --dir /path/to/project
```

The installer will not overwrite an existing skill. Cursor is installed project-locally at `.cursor/skills/fujisan-api-docs`, so `--dir` is required. Codex is installed into `$CODEX_HOME/skills` and Claude Code into `$CLAUDE_CONFIG_DIR/skills`, falling back to `~/.codex` and `~/.claude` when those variables are unset.

## Credentials for live requests

Keep the documentation account in `~/.config/fujisan/apidoc.env`, outside any repository, readable only by you:

```sh
mkdir -p ~/.config/fujisan
printf 'APIDOC_BASIC_USERNAME=%s\nAPIDOC_BASIC_PASSWORD=%s\n' "$user" "$password" > ~/.config/fujisan/apidoc.env
chmod 600 ~/.config/fujisan/apidoc.env
```

`scripts/with-apidoc-creds.sh` loads that file and runs a command with the credentials in its environment. They never appear in argv, shell history, or the script's output. The wrapper refuses to run when the file is readable beyond its owner. Set `APIDOC_ENV_FILE` to use a different path.

```sh
scripts/with-apidoc-creds.sh python3 skill/scripts/fetch_apidoc.py /api-index.json
```

## Local validation

```sh
npm test
python3 skill/scripts/fetch_apidoc.py /not-an-allowed-path
node bin/install.js --target cursor --dir /tmp/example-project
```
