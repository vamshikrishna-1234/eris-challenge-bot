This raw upload contains real AMI meeting-speech clips for a disfluency repair-structure benchmark.
clips.csv has one row per clipped WAV in audio/. Token transcripts are normalized word lists with implicit 0-based indices.
Positive labels come from AMI automaticSG_MAN repeat annotations with explicit reparandum and reparans nodes aligned to manual word timings.
Negative rows are real transcript windows without a structured repeat-repair target, including emphatic repeats, filler-only windows, and clean speech windows.
