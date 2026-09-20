# Reviewer premortem — Rail Corridor Incident And Dispatch Ledger Recovery

Written during scouting, before the package was finished, as the batch rules require.

**1. What is the closest source benchmark and why is this a different learning problem?**
The source (Fintraffic Digitraffic open railway data) carries no canonical ML benchmark. The closest
published tasks on railway operating data are forward delay prediction and primary/secondary delay
separation. This challenge is the inverse: from realized-versus-planned stop times across a
capacity-constrained corridor, recover the located, timed, typed incident ledger, the dispatcher's
holds, short-turns and cancellations, and the per-service primary cause.

**2. What is the closest local or platform semantic cluster and why will originality survive?**
`Ops-Log Causal-Chain Reconstruction From Raw Incident Telemetry` and `Stir Schedule Retrodiction From
Dye Mixing Pattern` on the platform; `Latent Market Contagion Graph and Intervention Ledger Recovery`
and `Grid Balancing Action Portfolio` in the registry. Railway, timetable, headway, junction,
disruption and outage all score zero hits across 3,087 platform titles and 92 registry entries. The
scored object - a matched incident ledger plus a dispatch trace plus a per-service attribution over a
scheduled network with capacity constraints - has no counterpart in either map.

**3. What native artifact supplies every scored field?**
Every scored field is produced by the corridor operations model in `prepare.py`, which is the
definition of ground truth for this challenge: the incident program it draws, the dispatch decisions it
takes, and the cause chain it records. The real published artifacts supply the world the model runs in
- station list, stop sequences, planned times, service classes and segment traffic - all taken
unchanged from the official API. The challenge does not claim the realized times or the ledger are
observations of real incidents; `SOURCE_VERIFICATION.md` and the dataset card state exactly which
fields are real and which are modelled.

**4. How many usable rows and independent hidden groups remain after every filter?**
Measured on the real prepared split: 2,400 train cases / 322,506 public observation rows and 800 test
cases / 55,781 rows, drawn from 49 usable corridors split 29 train / 20 hidden. `prepare.py` asserts at
least 24 usable corridors, at least 10 hidden corridors, at least 25 test occurrences of every incident
type and of each of NONE, SHORT_TURNED and CANCELLED.

**5. Why is every input modality necessary? Report ablations.**
Three signals are required and none is redundant: planned times (without them no deviation is
definable), realized times (the only evidence of what happened) and the corridor/capacity structure -
station index order, direction and service class - which is what separates a knock-on hold from a
primary incident. The ablation is the measured metadata-only attack: a predictor that sees the planned
timetable and corridor structure but no realized times cannot beat the label prior, because the hidden
program is drawn independently of the plan.

**6. How does a no-op, copied input, empty output and one-head-only output score?**
Measured with the canonical grader on the real split: empty or all-NONE 0.1237; label prior (the
shipped sample submission) 0.1685; incident head oracle alone 0.6237; intervention head oracle alone
0.3522; primary head oracle alone 0.2716; perfect exactly 1.0000. No no-op retains substantial credit,
and no single head can be ignored without losing its full weight.

**7. What capable solver is most likely to break the task, and what measured score did it obtain?**
A feature-engineered gradient-boosted structured predictor over per-segment excess running time,
per-station excess dwell and per-service delay trajectories - the route a capable agent takes on a
1.5 h CPU budget. Measured below, together with the achievable ceiling obtained by running the same
solver on a noise-free, dropout-free observation channel for the identical hidden programs.

**8. Can the public source recover hidden answers by exact, fuzzy, geometric, temporal or signal
retrieval?**
Measured as a two-stage attack at the shipped bundle size (one case = one corridor-window bundle of
whole services). Stage 1 de-anonymises the bundle back to its real corridor, date and window - it is
expected to succeed, because the published planned times are genuinely real. Stage 2 then re-attacks
the hidden ledger with the origin known, using the real recorded delays and the real official delay
causes for exactly those services and stops. Results in `LOOKUP_ATTACK_RESULTS.json`. The design
intent is that stage 1 buys the attacker nothing, because the scored ledger is a private construction
that exists in no public record.

**9. Can the exact raw package be imported now, within the size and licence rules?**
Yes. Ten official API responses, ~200 MB uncompressed, a flat `raw_upload.zip` far below the size at
which the platform upload server stalls. CC BY 4.0 with commercial use and redistribution explicitly
permitted; attribution and a modification notice ship in the archive and the dataset card.

**10. What single result would still force rejection?**
Stage 2 of the reversibility attack scoring materially above the label-prior floor, which would mean
the real public record does carry the hidden ledger after all. Second: the capability-matched baseline
landing close to the measured achievable ceiling, which would mean the task is saturated for a capable
solver rather than merely hard.
