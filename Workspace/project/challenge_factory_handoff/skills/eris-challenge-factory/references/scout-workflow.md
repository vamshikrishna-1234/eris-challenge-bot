# Scout Workflow

## Objective

Find a small number of genuinely different, source-verifiable challenges. Prefer one excellent survivor over a long shallow list.

## Procedure

1. Read the current platform constraints, local rules, previous reviews, accepted examples, idea inventories, output folders, and registry.
2. Build a compact duplicate map using both titles and semantic signatures:
   - input modalities;
   - target object;
   - supervision source;
   - output type and schema;
   - metric family;
   - likely solver family.
3. Search datasets before forcing a task idea when the user requests dataset-first research.
4. Open the official dataset page, license, paper, and actual archive/file listing. Inspect representative files or rows.
5. Prefer underused sources with useful native structure, but never treat low download count alone as novelty.
6. Formulate a real workflow that the native source can objectively support. Do not create creator-defined labels merely to make the output look richer.
7. Compare against the source's canonical task and nearest public benchmarks. Changing the title, metric weights, split, or JSON wrapper is not a substantive difference.
8. Estimate source size, prepared size, CPU training/inference time, memory, and simple baseline difficulty.
9. Reject candidates with nonpermissive or unclear redistribution, unavoidable lookup leakage, missing labels, standard classification/regression framing, impractical source size, or likely trivial scores.
10. Present only surviving ideas with explicit caveats and pilot gates.

## Candidate Report

For each survivor report:

- challenge title;
- one-sentence plain-language task;
- real-world use;
- exact input and output;
- one concrete sample;
- official dataset and direct source link;
- license and redistribution conclusion;
- raw and prepared size estimate;
- CPU approach and runtime estimate;
- nearest benchmark/local challenge;
- substantive novelty difference;
- natural difficulty mechanism;
- leakage and source-retrieval risks;
- mandatory pilot baselines;
- proceed, hold, redesign, or reject verdict.

## CPU-Only Default Gate

Unless current rules say otherwise, design for 10 CPU cores, 62 GB RAM, and a 1.5-hour solution limit. Avoid tasks whose credible solution requires training a large transformer, diffusion model, large detector, or full-resolution video model. Suitable routes include compact CNNs/TCNs, frozen small embeddings, tree/linear models over learned signals, DSP, graph algorithms, dynamic programming, and lightweight sequence models.

CPU feasibility does not excuse a plain tabular, scalar regression, or ordinary classification challenge.

## Difficulty Pilot

Specify measurable rejection gates before building. At minimum test:

- sample/prior output;
- metadata-only;
- source lookup or fingerprinting;
- simple parser/rule/DSP baseline;
- strongest obvious open-source baseline;
- intended multimodal or structured model;
- perfect oracle.

If an obvious baseline already exceeds the desired challenge range, change the core task or reject it. Do not compensate with arbitrary grader shaping.
