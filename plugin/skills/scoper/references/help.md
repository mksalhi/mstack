# Scoper help

Do not change mode or write flag files.

Levels
- Lite — `/mstack:scoper lite`: build asked; name one lazier alternative.
- Full — `/mstack:scoper full`: YAGNI→stdlib→native→one line→minimum. Default.
- Ultra — `/mstack:scoper ultra`: delete before add; challenge requirements.

Level sticks until changed or session end. Bare `/mstack:scoper`: if on, report; if off, turn on default unless default is `off` (then name a level).

Modes
- `/mstack:scoper`
- `/mstack:scoper review`
- `/mstack:scoper debt`

Deactivate: "stop scoper", "normal mode", or `/mstack:scoper off`. Resume: `/mstack:scoper`.

Default `full`, auto-active. Change:

Command
```
/mstack:scoper default lite|full|ultra|off
```
Environment variable
```bash
export SCOPER_DEFAULT_MODE=ultra
```
Config file (`~/.config/scoper/config.json`, Windows: `%APPDATA%\scoper\config.json`):
```json
{ "defaultMode": "lite" }
```
"off" disables auto-activation; activate with `/mstack:scoper`. Resolution: env var > config file > `full`.

Update: `/plugin marketplace update mstack`, then `/reload-plugins`.
