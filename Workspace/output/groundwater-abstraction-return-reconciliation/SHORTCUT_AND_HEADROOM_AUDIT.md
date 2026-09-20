# Shortcut and headroom audit — Groundwater Abstraction Return Reconciliation

All numbers below are produced by `_analyze.py` through the **shipped**
`grade.py` on the prepared split: **1,814 train / 686 test scenes, 8 hidden
score groups, 3 signal bands, background families disjoint across the split
(394 real wells in train, 154 in test).** Raw output: `analyze_results.json`,
`analyze.log`.

## 1. Baseline ladder

| Submission | Score | Notes |
|---|---|---|
| Perfect oracle | **1.0000** | upper bound of the metric |
| Achievable ceiling (true aquifer parameters + honest nonnegative rate recovery) | **0.6024** | measured on 180 test scenes; bounds what better parameter estimation can buy |
| Capability-matched solver (declared-anchored parameter search, then alternating nonnegative rate recovery and local parameter refinement) | **0.3152** | 180 scenes, 5.11 s/scene |
| Shipped `sample_submission.csv` (declared returns + cheap reference parameter fit) | **0.1451** | 686 scenes |
| Weak nonnegative least squares at fixed mid-range parameters | **0.0301** | 686 scenes, 0.03 s/scene |
| Uniform-random ledgers and parameters | **0.0055** | 686 scenes |
| Copy the declared returns (no-op) | **0.0001** | 686 scenes |
| Train-prior constant ledger | **0.0001** | 686 scenes |
| All-zero ledgers | **0.0000** | 686 scenes |
| Empty submission | **0.0000** | |

**Ceiling minus capability = 0.6024 − 0.3152 = 0.2872.**
**Capability minus the best trivial submission = 0.3152 − 0.0055 = 0.3097.**

The spread between the 0.03 s/scene route (0.0301) and the 5.1 s/scene route
(0.3152) is deliberate: both fit inside a 1.5-hour CPU budget over 686 scenes,
so the score separates modelling effort rather than compute luck.

## 2. Null-metric audit (batch Rule 5)

Every degenerate submission was scored before any baseline was believed.

- empty, all-zero, train-prior constant and copy-the-declaration all land at
  0.0000–0.0001.
- uniform random lands at 0.0055.
- Both scored heads are **rectified at group level, never per row**, so a lucky
  row cannot lift the floor. This was not true of the first two metric designs:
  a per-row rectified pooled metric gave uniform random **0.1577** and an
  all-zero submission **0.24**, and a corpus-pooled version still gave an empty
  submission **0.0937** because reporting zero abstraction repairs every
  over-declared borehole for free. The ledger head is now expressed as skill
  over the **best trivial strategy per borehole** (keep the declaration, or
  report no abstraction), which drove those three submissions to zero.
- A misdeclaration-**detection** head was measured and removed. On 40 held-out
  scenes no solver, including the capability-matched one, beat the best
  constant flagging rule (reference F1 0.539), so a weighted detection head
  would have been unreachable dead weight rather than a difficulty.

## 3. Grader red-team

| Attack | Score | Verdict |
|---|---|---|
| All ids shifted so nothing matches | 0.0000 | pass |
| `actual` replaced by the string `not json` | 0.1451 | expected: the ledger head goes to 0 and only the valid aquifer columns still score |
| `log_t` non-numeric and `log_s` NaN | 0.0000 | pass |
| `actual` filled with −5e9 | 0.1451 | expected, same reason as malformed JSON |
| Every row duplicated | 0.1451 | pass, identical to the clean sample (first row kept) |

`grade.py` never raises: every parse path degrades to zeros and the whole body
is wrapped so any unexpected condition returns 0.0. Declared theoretical
minimum **0.0** and maximum **1.0** match what the grader can actually return.

## 4. Source-retrieval attack (batch Rule 2), at shipped bundle size

Threat model, deliberately generous to the attacker: they hold the **exact**
pool of 548 conditioned real NWIS residual segments, including the train-family
segments, and they know the re-mixing family. They match each published
observation series by normalised maximum circular cross-correlation over every
shift, both time directions and both signs.

| Design | Top-1 recovery of the primary background source | Random expectation |
|---|---|---|
| Two-source mixing with shift/reversal/sign | 0.0833 | 0.00182 |
| **Shipped**: three sources, comparable random weights, independent linear time-warp per source | **0.00217** | 0.00182 |

460 probes. The shipped design is statistically indistinguishable from chance.

The deeper protection is structural: **the scored answer is the private
abstraction scene and the private aquifer parameters, which exist in no public
record.** A perfect background match would remove noise; it would not reveal a
single scored value. That is the property batch Rule 1 asks for.

## 5. Public-artifact leak scan

`_analyze.py` scans both public CSVs for column names carrying generation
state (`scene`, `bg_pool`, `rho`, `kind`, `background`, `site`, `nwis`, and the
answer fields on the test split). Result: **pass** for train and test. The raw
scene id, background pool tag, signal-to-noise ratio, declaration-error kind
and the actual ledgers are confined to `raw_data/scenes.csv` and
`private/answers.csv`; ids are fresh sequential integers assigned after a
deterministic shuffle, so row order carries no generation order.

## 6. Identifiability

The inverse problem was verified to be well posed before difficulty was tuned.
With the true aquifer parameters and noise-free observations, nonnegative rate
recovery scores **0.9805**, and the median design-matrix condition number is
**931**. An earlier formulation that asked for the free-space coordinates of an
unreported borehole was abandoned on measured evidence: Theis drawdown depends
on distance only logarithmically, median localisation error stayed near 600 m
in a 2,400 m domain, and rate and distance traded off almost exactly. Naming
the registered boreholes and asking which of them actually abstracted is both
the real regulatory workflow and the well-posed version of the question.

## 7. Capability-matched baseline construction (batch Rule 6)

The first capability-matched solver — a free nonnegative-least-squares search
over aquifer parameters feeding a sparse deconvolution — scored **0.15** and
lost to an all-zero submission, because free rate blocks absorb almost any
parameter pair and flatten the objective. It was **not** reported as the
ceiling. The principled version anchors the parameter search on the declared
returns, then alternates nonnegative rate recovery at fixed parameters with a
local parameter search at fixed rates; that is the standard type-curve and
superposition workflow, and it scores **0.3152**.
