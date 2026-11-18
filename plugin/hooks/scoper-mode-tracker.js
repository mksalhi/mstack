#!/usr/bin/env node
// scoper — UserPromptSubmit hook to track which scoper mode is active
// Inspects user input for /mstack:scoper commands and writes mode to flag file

const { getDefaultMode, isDeactivationCommand, normalizeMode, writeDefaultMode } = require('./scoper-config');
const { clearMode, readMode, setMode, writeHookOutput } = require('./scoper-runtime');

let input = '';
let done = false;

function switchTo(mode) {
  setMode(mode);
  writeHookOutput('UserPromptSubmit', mode, 'SCOPER MODE CHANGED — level: ' + mode);
}

function turnOff() {
  clearMode();
  writeHookOutput('UserPromptSubmit', 'off', 'SCOPER MODE OFF');
}

// Only `/mstack:scoper` (or `/scoper`, `$scoper`, `@scoper`) changes the mode.
// `/mstack:scoper review` and `/mstack:scoper debt` route to one-shot references
// and fall through as unknown arguments, so they leave the session mode alone.
function handleScoperCommand(prompt) {
  const parts = prompt.split(/\s+/);
  const cmd = parts[0].replace(/^[@$]/, '/').replace(/^\/mstack:/, '/');
  if (cmd !== '/scoper') return false;
  const arg = parts[1] || '';

  // `default <mode>` persists to config for new sessions; plain switches stay
  // session-scoped.
  if (arg === 'default') {
    const dmode = normalizeMode(parts[2]);
    if (dmode) {
      writeDefaultMode(dmode);
      writeHookOutput('UserPromptSubmit', dmode, 'SCOPER DEFAULT SET — new sessions start in ' + dmode + '.');
    }
    return true;
  }

  if (arg === 'off') {
    turnOff();
    return true;
  }

  if (arg === 'lite' || arg === 'full' || arg === 'ultra') {
    switchTo(arg);
    return true;
  }

  if (arg === '') {
    const current = readMode();
    if (current) {
      writeHookOutput('UserPromptSubmit', current, 'SCOPER MODE ACTIVE — level: ' + current);
      return true;
    }
    const fallback = getDefaultMode();
    if (fallback !== 'off') switchTo(fallback);
    return true;
  }

  // Unknown argument (e.g. `help`): keep the current mode.
  return true;
}

function finish() {
  if (done) return;
  done = true;
  try {
    // Strip UTF-8 BOM some shells prepend when piping (breaks JSON.parse)
    const data = JSON.parse(input.replace(/^﻿/, ''));
    const prompt = (data.prompt || '').trim().toLowerCase();

    if (/^[/@$](mstack:)?scoper/.test(prompt) && handleScoperCommand(prompt)) return;

    if (isDeactivationCommand(prompt)) turnOff();
  } catch (e) {
    // Silent fail
  }
}

process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', finish);

// Never hang the session. On Windows, Claude Code runs this hook through a
// PowerShell `if {}` wrapper that can swallow the piped prompt JSON, so stdin
// 'end' never fires and the hook would block forever. On error, or after a
// short fallback, process whatever arrived and exit. unref() keeps the timer
// from adding latency to the normal path, where 'end' fires first.
process.stdin.on('error', () => { finish(); process.exit(0); });
setTimeout(() => { finish(); process.exit(0); }, 1000).unref();
