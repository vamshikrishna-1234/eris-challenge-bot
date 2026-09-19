# Dataset creation form - fill-in

## Dataset name

```text
AMI Meeting Corpus Disfluency Source Subset
```

## Overview

This dataset is a bounded official-source subset of the AMI Meeting Corpus for spontaneous meeting-speech disfluency work. It contains extracted AMI manual annotation XML, extracted AMI automatic annotation XML, and twelve full headset-mix WAV recordings imported from the official AMI servers. The subset keeps the raw source artifacts only; it does not include derived clip tables or segmented audio examples.

## File structure

```text
ami_public_manual_1.6.2/       extracted official AMI manual annotations
ami_public_auto_1.5.1/         extracted official AMI automatic annotations
ES2002b.Mix-Headset.wav        official AMI headset-mix audio
ES2002c.Mix-Headset.wav        official AMI headset-mix audio
ES2006c.Mix-Headset.wav        official AMI headset-mix audio
ES2012b.Mix-Headset.wav        official AMI headset-mix audio
ES2012c.Mix-Headset.wav        official AMI headset-mix audio
IS1002b.Mix-Headset.wav        official AMI headset-mix audio
IS1004b.Mix-Headset.wav        official AMI headset-mix audio
IS1004c.Mix-Headset.wav        official AMI headset-mix audio
TS3006b.Mix-Headset.wav        official AMI headset-mix audio
TS3008c.Mix-Headset.wav        official AMI headset-mix audio
TS3009b.Mix-Headset.wav        official AMI headset-mix audio
TS3009d.Mix-Headset.wav        official AMI headset-mix audio
```

* `ami_public_manual_1.6.2/` contains AMI manual XML annotations after the official manual archive is imported and extracted.
* `ami_public_auto_1.5.1/` contains AMI automatic XML annotations after the official automatic archive is imported and extracted.
* The twelve `*.Mix-Headset.wav` files are official full headset-mix meeting recordings for the bounded source subset.
* No local archive file is part of this real-source dataset.

## Source annotation contents

`ami_public_manual_1.6.2/words/*.words.xml` contains word-level transcript entries. Relevant XML attributes include `starttime` and `endtime` for word timing, an AMI/NITE word id, punctuation markers, and word text.

`ami_public_auto_1.5.1/disfluency/automaticSG_MAN/*.disfluency.xml` contains automatic disfluency annotation XML aligned to AMI manual word ids. Relevant XML nodes include disfluency spans, child word references, and pointers to disfluency type definitions.

`ami_public_auto_1.5.1/ontologies/dsfl-types.xml` defines disfluency type labels used by the automatic annotations, including repeat, reparandum, and reparans-related labels.

The `*.Mix-Headset.wav` files are source audio recordings corresponding to the listed AMI meeting ids.

## Features

| Feature name | Type | Location | Description |
|---|---|---|---|
| `meeting_id` | string | filenames | AMI meeting id such as `ES2002b` or `TS3009d`. |
| `speaker_code` | string | XML filenames | AMI speaker stream code such as `A`, `B`, `C`, or `D`. |
| `word_id` | string | `words/*.words.xml` | NITE/AMI identifier for a transcript word element. |
| `word_text` | string | `words/*.words.xml` | Transcript token text stored as the XML word-node text. |
| `starttime` | float seconds | `words/*.words.xml` | Word start time in the source recording. |
| `endtime` | float seconds | `words/*.words.xml` | Word end time in the source recording. |
| `punc` | string/boolean | `words/*.words.xml` | AMI punctuation marker for word elements. |
| `disfluency_id` | string | `*.disfluency.xml` | NITE/AMI identifier for a disfluency XML node. |
| `dsfl_type_href` | string | `*.disfluency.xml` | Pointer from a disfluency node to a type definition. |
| `dsfl_type` | string | `dsfl-types.xml` | Disfluency type label such as repeat, reparandum, or reparans. |
| `child_word_href` | string | `*.disfluency.xml` | XML child reference linking a disfluency node to one or more word ids. |
| `wav_audio` | WAV binary | `*.Mix-Headset.wav` | Full headset-mix meeting audio recording. |

The XML files also contain additional AMI/NITE metadata fields. The fields above are the primary source features for transcript timing, disfluency structure, and audio alignment in this bounded subset.

## Audio format

The audio files are official AMI headset-mix WAV recordings. They are full meeting recordings, not pre-segmented examples. File sizes in this bounded subset range from about 63 MB to 77 MB per recording.

## License

CC BY 4.0. The official AMI license page states that the AMI corpus and annotations are released under Creative Commons Attribution 4.0, and the official AMI download page states that public signals, transcription, manual annotations, and automatic annotations are under CC BY 4.0.

## Source

Official AMI Corpus page: https://groups.inf.ed.ac.uk/ami/corpus/

Official AMI license page: https://groups.inf.ed.ac.uk/ami/corpus/license.shtml

Official AMI download page: https://groups.inf.ed.ac.uk/ami/download/

Official AMI transcription notes: https://groups.inf.ed.ac.uk/ami/corpus/transcription.shtml

Official AMI annotation overview: https://groups.inf.ed.ac.uk/ami/corpus/annotationpresent.shtml

Official AMI manual annotations: https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip

Official AMI automatic annotations: https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_auto_1.5.1.zip

## Notes

* The bounded official AMI source imports total 975,447,043 bytes, or about 930.3 MiB.
* The dataset contains raw source annotations and full source recordings only.
* The source subset includes AMI meeting families `ES`, `IS`, and `TS`.
