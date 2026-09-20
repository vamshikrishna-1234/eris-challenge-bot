# Lookup-gate evidence — candidate 3 `rail-corridor-incident-and-dispatch-ledger-recovery`

Measured verdict: **Pass**. Measured during scouting, at the shipped bundle size, with a two-stage
attack, as batch rule 2 requires.

## What the attacker is given

The shipped unit is a whole bundle, not a row: one case is one corridor-window bundle of complete
services. Measured on the real prepared split: **800 bundles, median 56 public rows and 7 complete
services per bundle**. The public corpus (the Fintraffic Digitraffic API) is fully available to the
attacker, including every real recorded arrival and departure time and every official delay-cause
record.

## Stage 1 — de-anonymise the bundle: granted to the attacker

The published planned times, stop sequences, service classes and corridor structure are genuinely
real. We do not claim bundle-level anonymity: a determined attacker willing to enumerate windows over
the public corpus can align a bundle back to its real corridor, date and window. **Stage 1 is
therefore granted at rank-1 = 1.000**, and stage 2 is run with the true corridor, date, window and
real service numbers handed over for free. That is strictly more conservative than any measured
stage-1 rate, and it removes the failure mode batch rule 2 warns about, where per-row resistance
evaporates once rows are bundled.

## Stage 2 — re-attack the hidden ledger with the origin known

| Measurement | Result |
|---|---|
| Real public rows carrying a recorded delay | 681,072 |
| Real services carrying an official delay-cause record | 4,369 |
| Published-vs-real delay, matched rows | 38,626 |
| Pearson r (published delay, real recorded delay) | **-0.0076** |
| De-anonymised real-corpus attacker, canonical grader | **0.1681** |
| Label-prior floor (the shipped sample submission) | 0.1668 |
| Chance floor (empty / all-NONE) | 0.1575 |
| Domain rule / DSP baseline, for scale | 0.3126 |

The attacker substitutes the **real** recorded operations of exactly those services and stops on
exactly that date for the published ones and runs the best domain rule available, then is scored
against the hidden ledger. It reaches 0.1681 against a label-prior floor of 0.1668 and a chance floor
of 0.1575. Handing the attacker the true origin and the whole real operating record of that day is
therefore worth **+0.0013 over simply guessing the modal incident type**, on a scale where the same
rule applied to the published rows scores 0.3126 and the perfect ledger scores 1.0. The workspace
precedent for a passing gate is about 2.5-3 % rank-1 origin recovery; here origin recovery is granted
in full and buys essentially nothing.

## Why the gate passes structurally, not by tuning

The scored ledger - the incident program, the dispatcher's holds, short-turns and cancellations, and
the per-service attribution - is constructed privately by `prepare.py` across the whole corpus. It
exists in no public record, so there is nothing to retrieve. What the public corpus does contain, the
planned timetable, is published to solvers anyway. The near-zero correlation between published and
real delays confirms the two are independent quantities rather than a transformed version of one
another.

This is the third candidate in this slot. Candidate 1 (wind SCADA) measured 12.5 % origin recovery and
candidate 2 (NHTSA CRSS) 8.8 % at its design floor, both because their scored target was a published
record of an identifiable public item. This candidate does not use a published record as its target,
which is why it passes by construction and why the measurement confirms rather than rescues it.

Script: `_lookup_attack.py`. Raw numbers: `LOOKUP_ATTACK_RESULTS.json`.
