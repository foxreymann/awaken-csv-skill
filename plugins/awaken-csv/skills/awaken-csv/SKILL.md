---
name: awaken-csv
description: Format crypto transaction or trade data into an Awaken.tax import CSV (standard, multi-asset, or futures/perpetuals format). Use this whenever the user wants to prepare, build, convert, or fix a CSV for Awaken.tax — e.g. turning exchange exports, on-chain transaction lists, trade history, staking/LP activity, or perps P&L into something Awaken can import. Trigger even if they don't say "Awaken" by name but mention formatting crypto transactions for tax import, or hand you raw trade data and ask for an importable CSV.
---

# Awaken.tax CSV formatting

Awaken.tax imports crypto transaction history from CSV. There are **three** CSV shapes, and the
hard part is (1) picking the right one, (2) getting the date/sign/decimal rules exactly right, and
(3) mapping each source row to the correct sent/received legs and tag. Get any of those wrong and
the import silently mis-computes gains/losses.

## Pick the format first

| Use this format | When the data is… | Header template |
| --- | --- | --- |
| **Standard** | Ordinary spot activity — one sent and/or one received asset per tx (buys, sells, swaps, transfers, deposits, withdrawals, income, airdrops). | `assets/template_standard.csv` |
| **Multi-asset** | A single tx moves **two+ assets on one side** — classically LP add/remove (send USDC + ETH, receive one LP token, or the reverse). | `assets/template_multi_asset.csv` |
| **Futures / Perps** | Perpetuals or futures trading where you track **P&L**, not asset legs (HyperLiquid, Jupiter Perps, etc.). | `assets/template_futures.csv` |

When in doubt between standard and multi-asset, use standard — only reach for multi-asset when a
single transaction genuinely has more than one asset on the same (sent or received) side. Most
exchange data is standard.

Read `references/labels-and-spec.md` for the full column-by-column detail and the complete tag enum
list. Read it before producing output unless this page already answers everything for the task.

If the source is an **exchange ledger** that splits one transaction across several rows sharing a
timestamp (Binance and similar), read `references/exchange-ledgers.md` — it covers the grouping,
sign, and spot-vs-futures traps, and points to a complete worked converter at
`scripts/binance-to-awaken.js`.

## Rules that must hold for every row

Read `references/validation-rules.md` for the complete, authoritative set of CSV validation rules
(date format, no-negatives, decimal precision, fee handling, header matching, re-import warning).
That file is the single source of truth — refer to it before producing output.

## Mapping each row

Decide the transaction type, then fill legs per the table in `references/validation-rules.md`
(section "Transaction-type leg rules"). Tag usage rules are also in that file (section "Tag column").

Read `references/labels-and-spec.md` for the complete tag enum and detailed per-label tax semantics.

## Workflow

1. Inspect the source data — columns, what each row represents, timezone, sign conventions, how
   fees are expressed.
2. Pick the format from the table above. If the data mixes spot and perps activity, split it into
   separate CSVs (one per format) — they can't share a header.
3. If anything material is ambiguous (timezone, which token is sent vs received, whether fees are
   already included in the amount, what a row's intent is), ask before guessing — a wrong mapping
   corrupts the tax math silently.
4. Produce the CSV using the matching template header. Keep business logic (the row mapping) separate
   from any display formatting, per project conventions.
5. **Write a companion findings `.md`** next to every CSV you generate (see below). This is required,
   not optional — the CSV is numbers, the `.md` is the audit trail for why those numbers are right.
6. Briefly report what you produced: which format, row count, any rows you couldn't confidently map,
   and any assumptions (e.g. "assumed source timestamps were UTC"). The chat report can be short
   because the detail lives in the `.md`.

## Companion findings doc

Every time you generate an Awaken CSV, also write a Markdown file capturing all findings and
decisions. Name it after the CSV's base name in the same directory: `ledgers/ftx.csv` →
`ledgers/ftx.md`. When one source produces several CSVs (e.g. a spot + a futures file), write **one**
combined `.md` under the shared base name covering all of them. The `.md` is the durable record a
future reader (or you, on the next export) needs to trust or reproduce the import without re-deriving
everything — write it for someone who has the raw export and the CSV but wasn't here for the
conversation.

Include, in this order:

- **Source & output** — which raw file(s) went in, which CSV(s) came out, the format chosen for each,
  and total row counts (input → output, so dropped/merged rows are visible).
- **Row-type mapping** — for each distinct source row type / transaction kind, how it maps to legs
  and which `Tag` it got. State the rule, not just the result (e.g. "fiat-quoted trades →
  `coin_buy`/`coin_sell`, crypto/stablecoin-quoted → `swap`").
- **Decisions & assumptions** — every judgment call and why: timezone conversion applied, how fees
  were attributed (on top vs included), gross-vs-net legs, what counts as internal/non-taxable and was
  skipped, stablecoin/fiat treatment, any deviation from a plan or from a default. Flag anything you
  guessed rather than confirmed.
- **Reconciliation** — the per-asset conservation/net check (see `references/exchange-ledgers.md`):
  what balanced, and every residual or imbalance with its likely cause (rounding dust, partial export
  window, pre-window balance, cross-account transfer). Negatives and non-zero nets must be named and
  explained, never silently left in.
- **Unmapped / uncertain rows** — anything you couldn't confidently map, and what you did with it.
- **Caveats** — re-import creates duplicates; missing-cost-basis assets Awaken will flag; data the
  export omits; anything the user should verify or supply.

Keep it factual and scannable (headings, short tables for the reconciliation). It should let the user
spot a wrong assumption without opening the CSV.

## Examples

**Standard — a swap of 10 USDC for 1 SOL on Solana, $0.0001 fee in SOL:**
```
Date,Received Quantity,Received Currency,Received Fiat Amount,Sent Quantity,Sent Currency,Sent Fiat Amount,Fee Amount,Fee Currency,Transaction Hash,Notes,Tag
09/30/2019 07:19:01,1,SOL,,10,USDC,,0.0001,SOL,,Swap on Jupiter,swap
```

**Standard — received 500 LOOKS as an airdrop (income, no sent leg):**
```
Date,Received Quantity,Received Currency,Received Fiat Amount,Sent Quantity,Sent Currency,Sent Fiat Amount,Fee Amount,Fee Currency,Transaction Hash,Notes,Tag
09/30/2019 07:19:01,500,LOOKS,2500,,,,,,,Airdrop,airdrop
```

**Multi-asset — sent 10 USDC + 1 SOL into an LP, got back 5 USDC-SOL-LP:**
```
Date,Received Quantity,Received Currency,Received Fiat Amount,Sent Quantity,Sent Currency,Sent Fiat Amount,Received Quantity 2,Received Currency 2,Sent Quantity 2,Sent Currency 2,Fee Amount,Fee Currency,Notes,Tag
09/30/2019 07:19:01,5,USDC-SOL-LP,,10,USDC,,,,1,SOL,,,Add liquidity,add_liquidity
```

**Futures — open then close a BTC short for +20 USDC:**
```
Date,Asset,Amount,Fee,P&L,Payment Token,ID,Notes,Tag,Transaction Hash
04/01/2024 00:00:00,BTC,1,0,0,,,Opened short,open_position,
04/02/2024 00:00:00,BTC,1,0.5,20,USDC,,Closed short,close_position,
```
