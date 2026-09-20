# Scout notes — batch-20260920-044727-task-001

## Duplicate map used
- Shipd archive titles (818 unique, 2026-09-15 scrape): `archive_titles.txt` in this folder.
- Bot registry (84 entries): dominant families = event-ledger-from-signal, graph induction, correspondence, decision reconstruction, partition/association, masked-interval trajectory, text-to-structure. Domains saturated in bot: meteorology/ocean/seismic, speech/audio, medical signals, crystallography/materials, maps, transit/maritime.
- Domains absent from both Shipd archive and bot registry: photography/camera settings, baseball, aviation ops, astronomy (mostly), typography, networking.

## Candidates considered (scout stage, no pilot)
- QuickDraw stroke-order recovery: already on Shipd ("Sketch Stroke Draw Order Prediction", "Drawing Stroke Assembly and Precedence Prediction"). Dropped.
- Wyscout soccer: Shipd "Territory: Field-Zone Estimation from Soccer Action Sequences". Dropped.
- Font kerning from glyph rasters: public-font retrieval recovers kerning tables exactly; unmitigable. Dropped.
- USPTO trademark design codes: plain hierarchical multi-label classification. Dropped.
- NASA DASHlink flight-recorder data: resource pages state "License N/A", site "for research purposes only"; redistribution unverifiable -> Hold-class, dropped.
- Wind turbine SCADA status ledger (Kelmarsh/Penmanshiel, CC BY 4.0): only 20 turbines / 2 sites; public 10-min series trivially retrievable by cross-correlation; event-ledger family already dense in bot. Dropped before pilot.
- Network Rail delay attribution: portal requires account; wiki blocked; unverified. Dropped.
- Lichess / chess: exact move sequences are a lookup key into public dumps. Dropped.

## Candidate 1 (piloted, REJECTED): baseball baserunner-advancement ledger (Retrosheet)
- Source: retrosheet.org event files 2022-2023 (also fetched 2018-2025), permissive notice license.
- Parser `pilot/rs_parse.py` validated by 3-outs-per-half-inning (only 6/43k short half innings).
- 104,205 batted-ball events with runners, 4,860 games. Coarse public tuple unique in only 5.98% of rows (lookup-safe).
- Measured: HistGradientBoosting pooled Brier skill 0.713 vs marginal reference (> 0.70 ceiling); situation prior alone 0.633 -> headroom ~0.16 (compressed). Fails toy-baseline/headroom gate. Evidence: `pilot/pilot_results.json`. Recorded with replace-candidate.

## Candidate 2 (piloting): photograph exposure-decision ledger (Wikimedia Commons CC0 / CC BY photos with native camera EXIF)
- Formulation: from the rendered photograph alone, recover the photographer's exposure ledger: ISO (stops), shutter (stops), aperture (stops), flash fired; possibly 35 mm-equivalent focal length.
- Native labels: camera-written EXIF (ISOSpeedRatings, ExposureTime, FNumber, Flash) on the original upload; selection by random API sampling (private, not replayable).
- License filter: CC0 and CC BY only (share-alike and PD-claims excluded).
- Family split: by photographer (Artist).
- Real workflow: archival metadata restoration for files with stripped EXIF; EXIF-consistency forensics; learned auto-exposure.
- Gates to measure in pilot: yield per API call, EXIF sanity, metadata-only baseline (aspect ratio), hand-feature GBM, pretrained-CNN-feature GBM, sample/prior score, per-head error distributions, photographer-family counts.

## Candidate 3 (piloted + built, REJECTED): half-inning play order reconstruction (Retrosheet 2005-2025)
- Task: recover the chronological order of the 5-7 plate appearances of an anonymized complete
  half inning from their unordered public descriptions plus the inning's line (events, runs).
- Source/licence/scale/independence gates all PASSED: 884,015 half innings parsed from 49,492 games
  over 21 seasons (0 unparsed plays after annotation stripping; 879,494 close on exactly three outs),
  225,208 admitted after the >=5-collision rule, shipped split 16,003/3,997 innings, family-disjoint.
- Metric designed to be permutation-invariant (identical descriptions never scored) and pooled, so
  uniform random = 0.0000, all-zeros = 0.0000, file order = 0.0032, perfect = 1.0000.
- Lookup PASSED but only to parity: unique public signature rate 0.59%, copy-one-twin attack 0.1445,
  strongest aggregate-twin attack 0.2309 at shipped bundle size 3,997 (median 932 candidates/row).
- REJECTED on headroom: sample 0.1841, outs-only 0.1830, marginal prior sort 0.2002, learned pairwise
  Borda 0.2280, constrained global decoder 0.2252. Separation 0.028, skill sweep flat
  (0.2208 / 0.2275 / 0.2280 at 10/30/100% of train). Richer vocabularies measured and worse
  (L1 gap 0.0348, L0 gap 0.0174; +LOB only 0.0433). Package retained as evidence, registry = rejected.

## Post-mortem against the batch rules (all three of my rejections)
- Candidate 1 (baseball baserunning): Rule 3 failure - 0.16 residual headroom, saturation.
- Candidate 2 (photo EXIF exposure): Rule 1 failure - the scored target was a per-image public
  sidecar, so learning signal and leakage channel were the same quantity.
- Candidate 3 (half-inning order): Rule 1 clean (combinatorial/generative, taught by the released
  split) and Rule 2 clean at bundle size, but Rule 3 failure - ceiling minus capability ~0.03.
- Lesson for the next candidate: pick a target whose *achievable ceiling* is demonstrably far above
  the best marginal-prior rule, and verify that on a bounded pilot BEFORE building anything (Rule 4).

## Ranked shortlist for candidate 4 (Rule-1 compliant, distinct from slots 2 and 3)
Slot 2 is scouting a private parameterised transformation over a real corpus; slot 3 holds a
wind-SCADA stop-event ledger. All three ideas below put the scored target in a structure that
`prepare.py` composes privately across many rows, so knowing any origin record does not reveal it.
1. **Multi-step reaction route recovery** from a public-domain reaction corpus (USPTO grants,
   e.g. the Lowe extraction): prepare.py privately composes k single-step reactions into a route,
   publishes only the endpoints plus a shuffled pool of candidate intermediates drawn from
   unrelated routes, and scores recovery of the intermediate chain. Learnable structure is
   chemistry (universal, taught by the training split); the composition is private, so locating
   any single public reaction does not give the route. CPU-feasible (fingerprints + trees).
   Measure first: chance floor for the restricted choice, achievable ceiling with a strong
   fingerprint retriever, and bundle-size de-anonymisation of the candidate pool.
2. **Private linear superposition of real measured signals**: sum m real traces from a permissive
   corpus with private weights and ask for the unmixing structure. Universal signal-level physics;
   answer defined by prepare.py's private mixture. Avoid turbine/SCADA and ECG (registry-dense).
3. **Corpus-level structural quantity**: target computed over many rows by prepare.py (e.g. a
   privately induced grouping/threshold), never a per-item public attribute.


## Candidate 4 (piloted, REJECTED): multi-step reaction route recovery (Lowe USPTO, CC0)
- Source clean: figshare 10.6084/m9.figshare.5104873, CC0 1.0, md5 verified, 1,808,937 reactions.
- Duplicate audit PASSED (no reaction-route task in 818 Shipd titles or 88 registry entries).
- REJECTED on Rule 2, decisively and by construction: prepare.py can only compose a route from
  single steps that are themselves public records. Canonical graph 691,464 molecules / 501,125
  edges. At shipped bundle size 4000 with a 40-item pool (chance floor 0.000641), two-sided public
  lookup recovered the full private route in 98.03% of rows; 96.75% of routes are the unique public
  3-step path; hardened pools infeasible (0.025% of routes have >=10 public successors and >=10
  predecessors). The same argument kills every per-record formulation over this corpus.
- Evidence: cand4/pilot/route_attack.json

## Candidate 5 (piloted + built, PROCEED): Groundwater Abstraction Return Reconciliation
- Real component: USGS NWIS instantaneous groundwater levels (parameter 72019), US Government
  public domain, 1,370 sites seen / 548 conditioned wells kept across 10 states.
- Generated component: Theis drawdown with superposition in time and space; private abstraction
  scenes, declaration errors and aquifer parameters. Declared honestly as a generated corpus over a
  real measured background (workspace rules explicitly support generate.py + raw_upload.zip).
- Rule 1: the scored answer exists in no public record, so identifying the background well reveals
  nothing; at worst it denoises.
- Rule 2: with the attacker handed the entire real pool, top-1 background recovery is 0.00217 vs a
  0.00182 chance rate (first design scored 0.0833 and was hardened with 3-source mixing + time-warp).
- Rule 5: three metric designs were measured. Per-row rectification gave uniform random 0.1577;
  corpus rectification still gave an empty submission 0.0937. The shipped ledger head is skill over
  the best trivial per-borehole strategy, and all degenerate submissions now score 0.0000-0.0055.
- Rule 6: the weak capability baseline (free-NNLS parameter search) scored 0.15 and lost to an
  all-zero submission; it was not reported. The principled alternating solver scores 0.3152.
- Final audited ladder (686 test scenes, 8 groups, disjoint background families): oracle 1.0000,
  ceiling with true aquifer parameters 0.6024, capability-matched 0.3152, shipped sample 0.1451,
  weak NNLS 0.0301, uniform random 0.0055, copy-declaration 0.0001, all-zeros/empty 0.0000.
  Ceiling minus capability 0.2872.
- An earlier free-coordinate formulation (locate an unreported borehole) was abandoned on measured
  evidence: Theis drawdown depends on distance only logarithmically, median localisation error
  ~600 m in a 2,400 m domain, and rate traded off against distance.

## Lesson carried forward
Candidates 1-4 all failed because the scored answer was recoverable from, or saturated by, public
records. Candidate 5 succeeds because the answer is a private physical scene: the public corpus can
teach the physics (and is published for exactly that purpose) but contains no instance of the answer.
