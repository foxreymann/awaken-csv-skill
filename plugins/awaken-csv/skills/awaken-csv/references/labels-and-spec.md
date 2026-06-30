# Awaken.tax — full label reference & detailed spec

Authoritative source: https://help.awaken.tax/en/articles/10422149-how-to-format-your-csv-for-awaken-tax

## Table of contents
- [Tag enum values](#tag-enum-values) — paste these exact strings into the `Tag` column
- [What each label does to your taxes](#what-each-label-does)
- [Per-column detail (standard / multi-asset)](#per-column-detail)
- [Futures detail](#futures-detail)

---

## Tag enum values

The `Tag` column is optional, but when you set it, use the exact `enum` string (right side), not the
display name. Awaken matches on the enum.

```
"Add Liquidity"          = "add_liquidity"
"Remove Liquidity"       = "remove_liquidity"
"Coin Sell"              = "coin_sell"
"Coin Buy"               = "coin_buy"
"Swap"                   = "swap"
"Lend Swap"              = "lend_swap"
"Withdraw Swap"          = "withdraw_swap"
"Lend"                   = "lend"
"Lend Borrow"            = "lend_borrow"
"Withdraw"               = "withdraw"
"Borrow"                 = "borrow"
"Repay"                  = "repay"
"Repay Withdraw"         = "repay_withdraw"
"Staking"                = "staking"
"Staking Swap"           = "staking_swap"
"Unstaking Swap"         = "unstaking_swap"
"Claim Rewards"          = "claim_rewards"
"Unstaking"              = "unstaking"
"NFT Buy"                = "nft_buy"
"NFT Sell"               = "nft_sell"
"NFT Swap"               = "nft_swap"
"Airdrop"                = "airdrop"
"Donation"               = "donation"
"Gift"                   = "gift"
"Non-Taxable"            = "non_taxable"
"Save For Later"         = "save_for_later"
"Income"                 = "income"
"Rewards Income"         = "rewards_income"
"Internal Transfer"      = "internal_transfer"
"External Transfer"      = "external_transfer"
"Spam"                   = "spam"
"Receive"                = "receive"
"Payment"                = "payment"
"Wrapping"               = "wrapping"
"Bridging"               = "bridging"
"Fee Expense Deduction"  = "fee_expense_deduction"
"Capital Gain"           = "capital_gain"
"Mining Income"          = "mining_income"
"Income Expense"         = "income_expense"
"Open Position"          = "open_position"
"Close Position"         = "close_position"
"Funding Payment"        = "funding_payment"
"Liquidation"            = "liquidation"
```

---

## What each label does

Use this to pick the right tag when the source data tells you the intent. If intent is unknown,
leave `Tag` empty — Awaken will auto-classify based on the sent/received pattern.

### Trading
- **Coin Swap / Exchange (`swap`)**: sale of one token for another. Realizes gain/loss on the sent token; fees add to cost basis of received.
- **Coin Buy (`coin_buy`)**: you receive a token with no sent token in the tx.
- **Coin Sell (`coin_sell`)**: you send a token with no received token in the tx. Realizes gain/loss on the sent token.
- **NFT Swap / Buy / Sell (`nft_swap` / `nft_buy` / `nft_sell`)**: NFT equivalents of the above.

### Staking & LP
- **Staking Deposit (`staking`)**: deposit into a staking protocol; no gain/loss on deposited tokens. Fees → Rewards Expenses.
- **Staking Swap (`staking_swap`)** / **Unstaking Swap (`unstaking_swap`)**: sale of one token for a derivative (ETH → stETH and back). Full gain/loss on sent.
- **Claim Rewards (`claim_rewards`)**: claimed assets treated as ordinary income at receipt price.
- **Unstaking (`unstaking`)**: withdraw from staking; original deposit returns with carried cost basis, surplus treated as income.
- **Add Liquidity (`add_liquidity`)** / **Remove Liquidity (`remove_liquidity`)**: sale of tokens for an LP token (and back). Full gain/loss on sent.
- **Wrapping (`wrapping`)**: wrap/unwrap via the wrapping contract. Toggleable as non-taxable in settings.

### Loans
- **Lend (`lend`)** / **Unlend / Withdraw (`withdraw`)**: lent assets are collateral, no gain/loss; cost basis transfers back on withdraw. Fees realize gain/loss.
- **Lend Swap (`lend_swap`)** / **Withdraw Swap (`withdraw_swap`)**: trading ETH ↔ aETH style. Gain/loss on all sent assets.
- **Borrow (`borrow`)** / **Repay (`repay`)**: no gain/loss on borrowed/repaid assets; tracked as Loan Liability.

### Friends & businesses
- **Receive (`receive`)**: crypto received from a wallet you own; non-taxable (same as wallet transfer).
- **Payment (`payment`)**: spending crypto on goods; sent tokens realize gain/loss.
- **Donation (`donation`)**: donation to a qualified non-profit; logged as Donation Expense at value.
- **Gift (`gift`)**: gifts to/from friends; not taxed.

### Income
- **Airdrop (`airdrop`)**: received assets taxed as income at receipt.
- **Income (`income`)**: paid in crypto (salary, services). Taxed as income.
- **Rewards Income (`rewards_income`)**: royalties/protocol rewards as income (non-staking).
- **Mining Income (`mining_income`)**: received assets as income.
- **Spam (`spam`)**: $0 cost basis, filtered out of history.
- **Income Expense (`income_expense`)**: an expense that offsets income.

### Transfers
- **Bridging (`bridging`)**: same asset across chains. Taxable disposal by default (toggleable).
- **Internal / Wallet transfer (`internal_transfer`)**: non-taxable transfer between your own wallets.
- **External Transfer (`external_transfer`)**: transfer to an external party.

### Other
- **Non-Taxable (`non_taxable`)**: no gain/loss on tokens sent/received (fees still realize gain/loss).
- **Fee Expense Deduction (`fee_expense_deduction`)**: offsets capital gains by the value of the asset at tx time.

> Note: all fees realize gain/loss at tx time — using crypto to pay a fee is effectively selling it.

---

## Per-column detail

Used by the **standard** and **multi-asset** formats.

| Column | Meaning |
| --- | --- |
| `Date` | See `validation-rules.md` → Date |
| `Received Quantity [n]` | Amount of token received, net of fees |
| `Received Currency [n]` | Ticker received, e.g. `SOL` |
| `Received Fiat Amount [n]` | (Optional) USD value at time received |
| `Sent Quantity [n]` | Amount of token sent, **excluding transfer fees** |
| `Sent Currency [n]` | Ticker sent |
| `Sent Fiat Amount [n]` | (Optional) USD value at time sent |
| `Fee Amount` | Fee paid (positive number) |
| `Fee Currency` | Ticker/fiat the fee was paid in |
| `Transaction Hash` | (Optional) tx hash → block-explorer links |
| `Notes` | (Optional) free text |
| `Tag` | (Optional) enum from the list above |

The `[n]` suffix (`Received Quantity 2`, `Sent Currency 2`, …) lets one transaction carry multiple
sent or received assets — needed for LP deposits/withdrawals where you send two tokens and get one
LP token back, or vice versa.

For transaction-type leg rules (which columns to fill for send/receive/trade) and fee handling
examples, see `validation-rules.md`.

---

## Futures detail

The perpetuals/futures format is different — it models P&L, not asset legs.

| Column | Meaning |
| --- | --- |
| `Date` | See `validation-rules.md` → Date |
| `Asset` | Underlying perp asset, e.g. `BTC`, `Fartcoin` |
| `Amount` | Amount of the underlying asset |
| `Fee` | Fee, denominated in the Payment Token |
| `P&L` | Net P&L of the trade — see `validation-rules.md` → No negatives |
| `Payment Token` | Token P&L settles in — usually `USDC`/`USDT` or a fiat |
| `ID` | (Optional) identifier for the trade |
| `Notes` | (Optional) |
| `Tag` | `open_position`, `close_position`, or `funding_payment` |
| `Transaction Hash` | (Optional) tx hash |

Worked example (from the docs):
- Open a short of 2 BTC → `Asset` BTC, `Amount` 1, `P&L` 0, `Tag` open_position
- Close 1 BTC short for +20 USDC → `Asset` BTC, `Amount` 1, `P&L` 20, `Payment Token` USDC, `Tag` close_position
- Receive a $10 funding payment → `Asset` USDC, `Amount` 10, `P&L` 10, `Payment Token` USDC, `Tag` funding_payment

For the no-negatives rule and its P&L exception, see `validation-rules.md` → No negatives.
