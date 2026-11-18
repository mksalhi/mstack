# Scoper help

Show this card when asked. Do not change mode or write flag files.

## Levels

| Level | Trigger | What change |
|-------|---------|-------------|
| **Lite** | `/mstack:scoper lite` | Build what's asked, name the lazier alternative in one line. |
| **Full** | `/mstack:scoper full` | The ladder enforced: YAGNI → stdlib → native → one line → minimum. Default. |
| **Ultra** | `/mstack:scoper ultra` | YAGNI extremist. Deletion before addition. Challenges requirements before building. |

Level sticks until changed or session end. Bare `/mstack:scoper` reports the current level when scoper is on. When it is off, bare `/mstack:scoper` turns on the default level, unless the default is `off`; then name a level.

## Modes

| Trigger | What it does |
|---------|--------------|
| `/mstack:scoper` | Lazy mode itself. Simplest solution that works. |
| `/mstack:scoper review` | Over-engineering review of a diff, or the whole repo with no diff: `L42: yagni: factory, one product. Inline.` |
| `/mstack:scoper debt` | Harvest `scoper:` shortcut comments into a tracked ledger. |

## Deactivate

"stop scoper", "normal mode", or `/mstack:scoper off`. Resume with `/mstack:scoper`.

## Configure the default mode

Default `full`, auto-active every session. Change it with:

**Command** (writes the config file below; applies to new sessions):
```
/mstack:scoper default lite|full|ultra|off
```

**Environment variable** (highest priority):
```bash
export SCOPER_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/scoper/config.json`, Windows: `%APPDATA%\scoper\config.json`):
```json
{ "defaultMode": "lite" }
```

`"off"` disables auto-activation; activate with `/mstack:scoper`. Resolution: env var > config file > `full`.

## Update

Ships inside mstack: `/plugin marketplace update mstack`, then `/reload-plugins`.

