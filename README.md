# Fujisan Agent Skills

This repository contains the following Agent Skills:

- `fujisan-api`
- `opensearch`
- `nagios-history`
- `nagios-investigate`
- `nagios-triage`
- `nagios-tune`

## List available skills

The [skills CLI](https://github.com/vercel-labs/skills) requires Node.js 22.20.0 or later. Use `--full-depth` to include the Nagios skills under `nagios/.cursor/skills/`:

```sh
npx skills add fujisanmagazine/ai-skills --list --full-depth
```

On a machine using Node.js 20, run the CLI with a temporary compatible Node.js version:

```sh
npx --yes --package=node@22.20.0 --package=skills -- skills add fujisanmagazine/ai-skills --list --full-depth
```

Until these changes reach the default branch, append `#feature/opensearch-poundsyslog-readonly` to `fujisanmagazine/ai-skills` in either command.

The repository is private, so the installing machine needs GitHub Read access. See each skill's README for authentication and installation instructions.
