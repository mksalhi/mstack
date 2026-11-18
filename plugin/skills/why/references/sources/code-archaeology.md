# Code Archaeology (git + in-repo)

## How to search it

```bash
git log --follow --oneline -- <file>
git log -S '<exact_string_from_code>' -- <file>
git log -G '<regex>' -- <file>
git blame -L <start>,<end> <file>
git log <old>..<new> -p -- <file>
```

Out-of-band docs:

```bash
rg -l -i 'architecture.decision' --glob '*.md'
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>
rg -l '<symbol>' --glob '*test*'
```
