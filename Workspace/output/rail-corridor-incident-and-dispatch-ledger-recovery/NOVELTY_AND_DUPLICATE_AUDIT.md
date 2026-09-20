# Novelty and duplicate audit — Rail Corridor Incident And Dispatch Ledger Recovery

## Method

- Local registry: all 92 entries in `Workspace/project/challenge_registry/` read and indexed by title,
  status, domain, modality, scored object.
- Platform archive: `Workspace/project/_all_challenge_titles.txt` is a mixed binary/text dump; 3,087
  genuine `## ` challenge titles were extracted and keyword-scanned.
- Semantic signature compared on all six axes: input modality, target object, supervision source,
  output schema, metric family, likely solver family.

## Coverage of this domain in both maps

Keyword hits across the 3,087 platform titles:

| Keyword | Hits |
|---|---|
| railway / rail operations | 0 |
| timetable | 0 |
| headway | 0 |
| junction | 0 |
| disruption | 0 |
| outage | 0 |
| schedule / scheduling | 1 (Stir Schedule Retrodiction From Dye Mixing Pattern) |
| dispatch | 2 (Cross-Modal Robot Dispatch; Dispatch State Vectors From Roadside Incident Clips) |
| delay | 2 (Argo Delayed-Mode QC; Guitar Note Continuation Under Delayed Monitoring) |

Registry hits for railway / timetable / dispatch: **0**.

## Nearest neighbours and the substantive difference

| Nearest item | Where | Why this challenge is a different learning problem |
|---|---|---|
| Ops-Log Causal-Chain Reconstruction From Raw Incident Telemetry | platform | IT incident telemetry to a causal chain. Here the input is a planned-versus-realized stop table over a capacity-constrained corridor, and the scored object additionally contains the dispatcher's own actions and a per-service cause attribution; the solver must reason about headway, single-track meets and knock-on propagation, not log causality. |
| Stir Schedule Retrodiction From Dye Mixing Pattern | platform | Closest structural analogue (recover a hidden schedule from its physical consequences) but a different domain, modality, output schema and solver family. |
| Latent Market Contagion Graph and Intervention Ledger Recovery | registry | Also an intervention ledger, but over a financial correlation graph; no capacity constraint, no schedule, no service-level attribution. |
| Grid Balancing Action Portfolio | registry | Operator-action recovery in electricity balancing; a portfolio of continuous actions, not a located, timed, typed incident ledger with a dispatch trace. |
| Anonymous Transit Vehicle Candidate Ranking | registry | Uses a transit feed, but the object is association of observations to vehicles. Here vehicle identity is given and the object is the hidden disruption program. |
| Train delay prediction / delay propagation literature (external) | external | The canonical task on railway operating data is *forecasting* delays forward. This challenge runs the inverse: given the realized deviations, recover the incidents that caused them, the dispatcher responses, and the per-service primary cause. |
| Primary/secondary delay separation (external) | external | The closest academic task. It separates a delay into primary and knock-on components; it does not localise, type, time or size the incidents, does not recover holds, short-turns and cancellations, and is not evaluated as a matched ledger. |

## Canonical-task check on the source

Fintraffic Digitraffic open data has no canonical ML benchmark task attached to it. It is an operational
open-data API, not a published benchmark. The two published quantities a benchmark could reuse - the
real `actualTime` and the real `causes` - are deliberately **not** used (see `SOURCE_VERIFICATION.md`),
so there is no reskin of an existing benchmark target.

## Originality-cluster risk and mitigation

The platform novelty checker scores from the title and opening prose. The title names the domain and
all three scored capabilities; the first paragraph of the description names the scored ledger and
explicitly rules out the nearest surrogate tasks (delay forecasting and primary/secondary separation)
rather than leaving the checker to find them. No source name, URL, DOI or licence name appears in the
participant-visible description.
