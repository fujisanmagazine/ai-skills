import assert from 'node:assert/strict';
import { existsSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { spawnSync } from 'node:child_process';

const scratch = () => mkdtempSync(join(tmpdir(), 'fujisan-api-docs-'));

const install = (args, env = {}) => spawnSync(process.execPath, ['bin/install.js', ...args], {
  cwd: new URL('..', import.meta.url),
  env: { ...process.env, ...env },
  encoding: 'utf8'
});

test('installs a Cursor skill into the selected project', () => {
  const project = scratch();
  const result = install(['--target', 'cursor', '--dir', project]);
  assert.equal(result.status, 0, result.stderr);
  assert.ok(existsSync(join(project, '.cursor', 'skills', 'fujisan-api-docs', 'SKILL.md')));
});

test('installs a Codex skill under CODEX_HOME', () => {
  const home = scratch();
  const result = install(['--target', 'codex'], { CODEX_HOME: home });
  assert.equal(result.status, 0, result.stderr);
  assert.ok(existsSync(join(home, 'skills', 'fujisan-api-docs', 'SKILL.md')));
});

test('installs a Claude Code skill under CLAUDE_CONFIG_DIR', () => {
  const home = scratch();
  const result = install(['--target', 'claude'], { CLAUDE_CONFIG_DIR: home });
  assert.equal(result.status, 0, result.stderr);
  assert.ok(existsSync(join(home, 'skills', 'fujisan-api-docs', 'scripts', 'fetch_apidoc.py')));
});

test('refuses to overwrite an existing skill', () => {
  const project = scratch();
  assert.equal(install(['--target', 'cursor', '--dir', project]).status, 0);
  const second = install(['--target', 'cursor', '--dir', project]);
  assert.equal(second.status, 1);
  assert.match(second.stderr, /Refusing to overwrite/);
});

test('rejects an unknown target and a Cursor install without --dir', () => {
  assert.equal(install(['--target', 'vscode']).status, 1);
  assert.equal(install(['--target', 'cursor']).status, 1);
  assert.equal(install([]).status, 1);
  assert.equal(install(['--help']).status, 0);
});
