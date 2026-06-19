# Privacy Policy

_Last updated: 2026-06-19_

## Summary

The **Awaken.tax CSV Formatter** plugin (the "Skill") is a set of instructions and
template files that run locally inside Claude Code. The Skill itself does **not**
collect, store, transmit, sell, or share any personal or financial data. It has no
backend, no servers, no analytics, and no network calls of its own.

## What the Skill does

The Skill instructs Claude Code to read transaction or trade data that **you** provide
(exchange exports, on-chain transaction lists, trade history, etc.) and reformat it into
an Awaken.tax import CSV, plus a companion findings document. All of this happens within
your local Claude Code session, against files on your own machine.

## Data handling

- **No data collection.** The Skill does not gather, log, or retain any information.
- **No transmission by the Skill.** The Skill does not send your data anywhere. Output
  files (the CSV and the `.md`) are written only to locations you direct, on your own
  machine.
- **Local processing.** Reading your input and writing the output occurs locally as part
  of your Claude Code session.

## Third parties

Although the Skill itself collects nothing, please be aware:

- **Claude Code / Anthropic.** The contents you ask Claude to process are handled by
  Claude Code and the underlying model provider (Anthropic) under their own terms and
  privacy policy. See <https://www.anthropic.com/legal/privacy>.
- **Awaken.tax.** The CSV produced by this Skill is intended to be imported into
  Awaken.tax. Any data you upload there is governed by Awaken's own privacy policy. This
  Skill is an independent, unofficial helper and is not affiliated with or endorsed by
  Awaken.tax.

## Sensitive financial data

Crypto transaction histories can be sensitive. The Skill is designed to work entirely on
your local data and to produce an auditable record of its decisions. You remain
responsible for where you store and share the generated files.

## Changes

This policy may be updated from time to time. Material changes will be reflected in this
file with an updated date.

## Contact

For questions about this Skill, open an issue at
<https://github.com/foxreymann/awaken-csv-skill/issues>.
