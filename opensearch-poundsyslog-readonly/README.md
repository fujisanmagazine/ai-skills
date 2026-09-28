# Fujisan Pound/OpenSearch Read-only Skill

This Agent Skill supports read-only investigations of pound access logs in the Fujisan OpenSearch cluster. It requires `OPENSEARCH_USER` and `OPENSEARCH_PASSWORD` in the workspace's `.env` file when the skill is used.

## Install

After this skill is pushed to GitHub, install it from the repository with the [skills CLI](https://github.com/vercel-labs/skills). The current CLI requires Node.js 22.20.0 or later. Each installer must have Read access to the private `fujisanmagazine/ai-skills` repository. On their own machine, they can authenticate and check access with:

```sh
gh auth login -h github.com --git-protocol https --web
gh auth status
gh repo view fujisanmagazine/ai-skills
```

If already signed in, skip `gh auth login`. If the organization requires SAML SSO, [authorize GitHub CLI's app for the organization](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-single-sign-on/authorizing-an-app-for-single-sign-on) as needed. Then run the command in the project where you want to use the skill:

```sh
npx skills add fujisanmagazine/ai-skills --skill opensearch-poundsyslog-readonly -a cursor -y
```

On a machine still using Node.js 20, run the CLI with a temporary compatible Node.js version:

```sh
npx --yes --package=node@22.20.0 --package=skills -- skills add fujisanmagazine/ai-skills --skill opensearch-poundsyslog-readonly -a cursor -y
```

Use `-a codex` or `-a claude-code` for those agents. Add `-g` to install globally instead of in the current project. The CLI can also use an existing Git credential helper or authorized SSH key.

No repository clone or npm package publication is needed.
