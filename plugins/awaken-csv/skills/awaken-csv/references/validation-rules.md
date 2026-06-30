# Awaken.tax — CSV validation rules

These rules apply to **all three** CSV formats (standard, multi-asset, futures) unless noted
otherwise. They come straight from Awaken's importer and are the usual source of silent errors.

## Date

- Must be in **UTC**. Convert from any source timezone first.
- Awaken accepts two forms:
  - Documented: `MM/DD/YYYY HH:MM:SS` (e.g. `09/30/2019 07:19:01`)
  - ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`
- This repo's existing ledgers under `ledgers/` use the ISO form — match that for consistency.
- The futures template additionally accepts bare `YYYY-MM-DD`.

## No negatives

- Quantities, amounts, and fees must be **non-negative** across all columns — the only exception
  is the futures `P&L` column, which can be negative, positive, or zero.
- If a source row has a negative amount, that signals direction (sent vs received) — encode it by
  which column you place it in, not with a minus sign.

## Decimal precision

- Up to **8 decimal places**. Don't pad with trailing zeros beyond what's meaningful.
- Never use scientific notation.
- This project stores amounts as BigInt with 8 decimals — convert to plain decimal strings for the
  CSV (see `@libs/bigint.js` `toDS()`).

## Fee handling

- Fees are **separate** from the sent amount.
- Example: 1 ETH transferred with a 0.1 ETH network fee →
  `Sent Quantity` = 0.9, `Fee Amount` = 0.1, `Fee Currency` = ETH — **not** 1.0 sent.
- One Awaken row has one fee slot. If a timestamp group has fees in two currencies, emit the extra
  fee as its own fee-only row rather than dropping it.

## Header

- The header row must match the template exactly — don't rename, reorder, or drop columns.

## Transaction-type leg rules

How to fill sent/received columns based on the type of activity:

| Activity | Sent columns | Received columns |
| --- | --- | --- |
| **Receive / deposit / income / airdrop** | Leave empty | Fill (net of fees) |
| **Send / withdrawal / sell / payment** | Fill (net of transfer fee) | Leave empty |
| **Trade / swap** | Fill | Fill |

## Tag column

- Optional. Set it from the enum in `labels-and-spec.md` **only when the source data makes the
  intent clear** (e.g. labelled "staking reward", "airdrop", "LP deposit").
- If intent is ambiguous, leave it empty and let Awaken auto-classify from the sent/received
  pattern — a wrong tag is worse than no tag.

## Re-import warning

Importing the same CSV twice creates duplicates. Mention this if the user might re-import.
