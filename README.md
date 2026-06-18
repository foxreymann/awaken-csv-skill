# Awaken.tax CSV Skill

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill that formats crypto transaction
and trade data into an [Awaken.tax](https://awaken.tax) import CSV — standard, multi-asset, or
futures/perpetuals format.

## Install

```
/plugin marketplace add foxreymann/awaken-csv-skill
/plugin install awaken-csv@awaken-csv-skill
```

Then just ask Claude to turn an exchange export, on-chain transaction list, or perps P&L into an
Awaken-importable CSV.

## What's inside

- `plugins/awaken-csv/` — the plugin
  - `skills/awaken-csv/SKILL.md` — the skill instructions
  - `skills/awaken-csv/references/` — format spec, label list, exchange ledger notes
  - `skills/awaken-csv/assets/` — CSV header templates

## License

MIT
