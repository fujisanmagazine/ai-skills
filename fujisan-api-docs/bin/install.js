#!/usr/bin/env node
import { cpSync, existsSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const usage = `Usage: fujisan-api-docs-skill --target <codex|claude|cursor> [--dir <project-dir>]\n\nFor Cursor, --dir is required and installs into <project-dir>/.cursor/skills.`;
const args = process.argv.slice(2);
const valueFor = (name) => {
  const index = args.indexOf(name);
  return index === -1 ? undefined : args[index + 1];
};
const target = valueFor('--target');
const projectDir = valueFor('--dir');

// Thunks, not values: the cursor root depends on --dir, which is absent for the other targets.
const skillRoots = {
  codex: () => resolve(process.env.CODEX_HOME || resolve(homedir(), '.codex'), 'skills'),
  claude: () => resolve(process.env.CLAUDE_CONFIG_DIR || resolve(homedir(), '.claude'), 'skills'),
  cursor: () => resolve(projectDir, '.cursor', 'skills')
};

if (!target || !Object.hasOwn(skillRoots, target) ||
    (target === 'cursor' && !projectDir) || args.includes('--help')) {
  console.error(usage);
  process.exit(args.includes('--help') ? 0 : 1);
}

const skillSource = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'skill');
const destination = resolve(skillRoots[target](), 'fujisan-api-docs');

if (existsSync(destination)) {
  console.error(`Refusing to overwrite existing skill: ${destination}`);
  process.exit(1);
}
mkdirSync(dirname(destination), { recursive: true });
cpSync(skillSource, destination, { recursive: true });
console.log(`Installed fujisan-api-docs for ${target}: ${destination}`);
