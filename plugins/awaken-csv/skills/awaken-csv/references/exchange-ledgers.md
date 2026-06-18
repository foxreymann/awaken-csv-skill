# Converting exchange "ledger" exports

Some exchanges (Binance is the classic case) don't export one row per transaction — they
export one row per **coin movement**, and a single economic transaction is split across
several rows that share a timestamp. A spot trade shows up as a `Sell` row + a `Buy` row +
a `Fee` row, all at the same `UTC_Time`. Converting these to Awaken's one-row-per-transaction
model is the hard part, and there are a few traps that quietly corrupt the numbers.

A complete, tested implementation lives at `scripts/binance-to-awaken.js` — read it as the
reference when handling a Binance export, or as a template for a different exchange's ledger.
Run it with `node scripts/binance-to-awaken.js [inputCsv] [outDir]` (defaults write the full
Binance history into `ledgers/tmp/`).

## The traps (learned the hard way on a real 69k-row export)

1. **Group by timestamp, then sum legs by coin.** Many exchanges split one order into several
   same-second fills (e.g. five `Buy` rows for one DCA order). Sum all legs of a coin within a
   timestamp group *before* deciding the shape — otherwise a clean swap explodes into a pile of
   disconnected `coin_sell`/`coin_buy` rows. Only when, after summing, there are genuinely 2+
   assets on one side (dust conversions, two unrelated trades in the same second) do you split.

2. **Trust the sign of the amount, never the operation name, for direction.** Exchanges are
   inconsistent — a row labeled `Send` or `Withdraw` can carry a *positive* change. If you
   hardcode "Send = outgoing" you flip the sign and the error is double the amount. Decide
   received-vs-sent purely from whether the change is positive or negative.

3. **Split spot and futures into separate CSVs.** Perps activity (realized P&L, funding,
   futures fees) belongs in the futures format; everything else in standard/multi-asset. They
   can't share a header. Note that a ledger export often lacks the futures *underlying asset and
   position size* — only the settlement-coin P&L is present — so the futures `Asset`/`Amount`
   columns can't be filled meaningfully; record the P&L and fees and document the gap.

4. **Futures fees don't all match a realized-P&L row.** You pay a fee opening *and* closing a
   position, but only the closing trade realizes P&L. So matching fees to P&L by trade id leaves
   most fees (the opening ones) unmatched — they're not orphans to discard, they're real costs.
   Keep them.

5. **One Awaken row has one fee slot.** If a timestamp group genuinely has fees in two
   currencies (two trades merged on the same second), emit the extra fee currency as its own
   fee-only row rather than dropping it.

## Always run a conservation check

The single most valuable test: for **every coin**, the sum of all input `Change` values must
equal what the output represents — `received − sent − fee` across the spot CSV, plus
`P&L − fee` across the futures CSV, plus anything you left unmapped. If a coin doesn't balance,
you've dropped, duplicated, or sign-flipped something. Bisect the mismatch by year, then by
timestamp, to find the offending rows. Getting all coins to conserve exactly is what gives you
confidence the import is faithful — do this before handing the CSV to the user.
