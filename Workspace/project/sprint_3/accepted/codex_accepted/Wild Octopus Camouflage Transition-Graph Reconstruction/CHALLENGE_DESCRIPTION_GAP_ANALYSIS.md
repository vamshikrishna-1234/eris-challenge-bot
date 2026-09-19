# Participant-description gap analysis

The available accepted computer-vision descriptions are in `shipd_domain_challenge_docs/Computer-Vision.md` (there are no literal `CV.txt` files). Their recurring requirements were applied to `CHALLENGE_FORM_FILL.md`:

- Overview and a dedicated Task subsection state the video input, structured graph output, real-world activity-understanding value, and held-out-session generalization contract.
- File-overview, train/test column, and submission tables are present with parser-friendly types and constraints.
- The Dataset section includes a parseable fenced CSV example with the submission header and three real template rows.
- The graph schema and allowed values are stated in plain prose as well as table context.
- Intended CPU approaches are explicitly allowed: frozen MobileNetV3/ResNet18 frame features, GRU/TCN/transformer-lite temporal decoding, constrained JSON generation, and ordinary augmentation.
- What-not-to-use and enforcement paragraphs explicitly reject ID/filename/row-order/file-size/archive/encoding side channels, public-source lookup, constants, metadata-only and rule-only solutions, detector-only differencing, and transductive hidden-label use.
- The description documents grouped held-out-session generalization, malformed-row behavior, structural invalid-submission errors, score range, oracle behavior, and weak-sample/headroom expectations.

The description does not name the upstream MEVA source or reveal source filenames, exact split groups, transform salts, or annotation URLs. Those details remain in organizer-only source documentation.
