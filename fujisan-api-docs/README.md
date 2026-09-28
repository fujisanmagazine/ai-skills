# Fujisan API Docs Skill

An Agent Skill for consulting the primary Fujisan API documentation. It reads only documentation resources from `https://apidoc.fujisan.co.jp/`; it does not call operational Fujisan APIs.

## Install

Install the skill from GitHub with the [skills CLI](https://github.com/vercel-labs/skills). The current CLI requires Node.js 22.20.0 or later. Each installer must have Read access to the private `fujisanmagazine/ai-skills` repository. On their own machine, they can authenticate and check access with:

```sh
gh auth login -h github.com --git-protocol https --web
gh auth status
gh repo view fujisanmagazine/ai-skills
```

If already signed in, skip `gh auth login`. If the organization requires SAML SSO, [authorize GitHub CLI's app for the organization](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-single-sign-on/authorizing-an-app-for-single-sign-on) as needed. Then run this command in the project where you want to use the skill:

```sh
npx skills add fujisanmagazine/ai-skills --skill fujisan-api-docs -a cursor -y
```

On a machine still using Node.js 20, run the CLI with a temporary compatible Node.js version:

```sh
npx --yes --package=node@22.20.0 --package=skills -- skills add fujisanmagazine/ai-skills --skill fujisan-api-docs -a cursor -y
```

Use `-a codex` or `-a claude-code` for those agents. Add `-g` to install globally instead of in the current project. The CLI can also use an existing Git credential helper or authorized SSH key. No manual repository clone or npm package publication is needed.

## Credentials for live requests

The documentation server uses Basic authentication. Set `APIDOC_BASIC_USERNAME` and `APIDOC_BASIC_PASSWORD` in the environment that runs the agent. Do not store them in project files or agent configuration.

Keep the documentation account in `~/.config/fujisan/apidoc.env`, outside any repository, readable only by you:

```sh
mkdir -p ~/.config/fujisan
printf 'APIDOC_BASIC_USERNAME=%s\nAPIDOC_BASIC_PASSWORD=%s\n' "$user" "$password" > ~/.config/fujisan/apidoc.env
chmod 600 ~/.config/fujisan/apidoc.env
```

The installed skill includes `scripts/with-apidoc-creds.sh`. It loads that file and runs a command with the credentials in its environment. They never appear in argv, shell history, or the script's output. The wrapper refuses to run when the file is readable beyond its owner. Set `APIDOC_ENV_FILE` to use a different path.

```sh
scripts/with-apidoc-creds.sh python3 scripts/fetch_apidoc.py /api-index.json
```

## Local validation

```sh
python3 -m unittest discover -s test
```
