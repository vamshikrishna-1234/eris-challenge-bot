# Build and novelty notes

## Why this is a distinct ML task

Nearest tasks and products include the operational lightning clustering algorithm itself, lightning detection, flash-rate estimation, storm tracking/nowcasting, and the NASA CIERRA reclustering dataset. The raw product already provides an event-to-group-to-flash tree, while CIERRA focuses on correcting operational cluster integrity and adding higher-order lightning objects.

This challenge does not ask participants to redetect lightning from imagery, forecast weather, track storm cells, complete a knowledge graph, or reproduce an operational fixed threshold in native units. It creates compact, transformed local point sets containing competing native flashes; removes absolute lookup context and native graph ids; and asks for joint recovery of both nested partitions plus calibrated abstention on detections that are boundary-ambiguous after redaction. The combination of hierarchical point-set induction, realistic overlapping decoys, label-invariant structured scoring, and explicit boundary uncertainty is the novelty. Estimated novelty: 6.5/10.

The duplicate scan covered existing sprint-3 output/build folders and the local Shipd domain challenge documents. No prior GLM, lightning-mapper, or event-to-group-to-flash hierarchy challenge was found. The closest local design was radar evidence-lineage repair, which has a different observation unit, target graph, and scientific source. Structure and safety conventions were compared against three accepted examples: switch-lamp logic induction, molecular mass-spectrum fingerprint prediction, and annotator reliability/adversarial-rater detection.

## Feasibility and shortcut gate

The held-out split consists of two complete source windows, 70 cases per window. Every source, density, and ambiguity subgroup in private data has at least 30 cases. See `ANALYSIS_RESULTS.json` for machine-readable results.

| Probe | Held-out score |
|---|---:|
| Native hierarchy oracle (sanity only) | 1.0000 |
| Metadata-only fixed partition | 0.1467 |
| Fixed prompt/schema only | 0.1467 |
| JSON-length/point-count attack | 0.1414 |
| Opaque-id row order | 0.1407 |
| Opaque-id hash | 0.1573 |
| Fixed operational-threshold surrogate | 0.2067 |
| Train-tuned DBSCAN grid | 0.2249 |
| Compact CPU pairwise model + decoder | 0.3406 |

The strongest measured shortcut leaves 77.51% absolute headroom to perfect, exceeding the required 30%. DBSCAN's flash-pair head is high because large-scale flash separation survives, but the metric now gives the easy coarse flash partition less weight. Its count-consistent group-pair score is only 0.1096, uncertainty F1 is 0.2191, exact rate is zero, and total score is 0.2249. The learned model improves group-pair F1 to 0.2724 and uncertainty F1 to 0.3577 while staying CPU-small, reaching 0.3406. This supports learnability without making fixed clustering sufficient.

## Split and ambiguity construction

Three complete source windows form train and two complete later windows form test. A source object never crosses the split. Each case combines two nearby native flashes, samples multiple native groups and their events, and publishes 12–40 detections. The public transform uses a deterministic per-case rotation/reflection, mild shear, robust spatial and time normalization, controlled jitter, energy ranking, and public-only neighborhood densities.

A detection is labeled uncertain when the nearest same-versus-different group or flash evidence has a small or inverted margin in the transformed public space. The selection threshold is case-local and capped, so ambiguity is derived from both native hierarchy truth and the evidence participants actually receive; it is not random noise.

The official product has group- and flash-level quality flags but no event-level quality score. Valid cases are restricted to good-quality native parents. Those flags are therefore nearly constant and parent-level; publishing them per detection would add no useful signal and could leak a hidden parent. They are used as source filters but intentionally omitted from the public detection schema.

## Known limitations

- Every prototype case contains two native flashes. This can be inferred from training labels and makes the coarse flash head easier, but it does not reveal the group hierarchy or boundary set; the metadata-only and threshold scores quantify the residual shortcut.
- The corpus is deliberately compact and samples only five short official source windows. Generalization is source-window held out, not a claim about all seasons, satellites, or storm regimes.
- Public coordinates are transformed local evidence, not a physically invertible coordinate system. They should not be used for scientific geolocation.
- The internal NetCDF license-string conflict is documented in `SOURCE_VERIFICATION.md`; the build relies on the official NODD dataset license and NCEI policy.
- No solver-agent or external autonomous solver run was used. `_analyze.py` contains the only trainable baseline.
