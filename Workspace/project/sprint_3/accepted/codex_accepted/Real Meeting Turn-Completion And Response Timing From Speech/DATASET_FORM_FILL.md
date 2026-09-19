# Dataset creation form - fill-in

## Dataset name

```text
AMI Meeting Corpus Headset Audio And Manual Annotations
```

## Overview

This dataset consists of official AMI Meeting Corpus source files imported directly from AMI URLs: one extracted manual annotation directory and a bounded set of real 16 kHz headset-mix meeting WAV files. The annotation directory contains AMI NXT XML word, segment, and dialogue-act annotation files, and the WAV files contain full real multi-party meeting recordings. No train/test splits or pre-extracted challenge clips are included in the uploaded raw data.

## File structure

```text
ami_public_manual_1.6.2/                  extracted AMI manual annotations
ami_public_manual_1.6.2/words/*.xml       word-level transcript annotations
ami_public_manual_1.6.2/segments/*.xml    segment and turn-region annotations
ami_public_manual_1.6.2/dialogueActs/*.xml dialogue-act annotations
ami_public_manual_1.6.2/LICENCE.txt       AMI CC BY 4.0 license text
EN2001a.Mix-Headset.wav                   official AMI meeting audio
ES2002a.Mix-Headset.wav                   official AMI meeting audio
ES2003a.Mix-Headset.wav                   official AMI meeting audio
ES2004a.Mix-Headset.wav                   official AMI meeting audio
IB4001.Mix-Headset.wav                    official AMI meeting audio
IN1001.Mix-Headset.wav                    official AMI meeting audio
IS1000a.Mix-Headset.wav                   official AMI meeting audio
TS3003a.Mix-Headset.wav                   official AMI meeting audio
```

* `ami_public_manual_1.6.2/` is the extracted official AMI manual annotation archive imported from AMI.
* `ami_public_manual_1.6.2/words/` contains per-meeting, per-speaker word transcript XML files.
* `ami_public_manual_1.6.2/segments/` contains per-meeting, per-speaker segment XML files that reference word ids.
* `ami_public_manual_1.6.2/dialogueActs/` contains dialogue-act XML files included in the official annotation archive.
* `*.Mix-Headset.wav` files are official AMI headset-mix WAV recordings imported directly from AMI.
* `ami_public_manual_1.6.2/LICENCE.txt` is the CC BY 4.0 license text bundled with the official annotation archive.

## Features

`*.Mix-Headset.wav` (WAV audio): full AMI meeting audio recording for one meeting. The meeting id is the filename prefix, for example `ES2002a`.

`words/*.words.xml` root id (string): AMI document id for one meeting-speaker word stream.

`words/*.words.xml` `w` element text (string): orthographic token text for a spoken word.

`words/*.words.xml` `w@nite:id` (string): unique AMI word id.

`words/*.words.xml` `w@starttime` (float seconds): word start time in the meeting recording.

`words/*.words.xml` `w@endtime` (float seconds): word end time in the meeting recording.

`words/*.words.xml` `w@punc` (boolean-like string, optional): marks punctuation tokens when present.

`words/*.words.xml` `vocalsound` element (XML element, optional): non-word vocal event such as laugh or other vocal sound, with timing and type attributes when annotated.

`segments/*.segments.xml` root id (string): AMI document id for one meeting-speaker segment stream.

`segments/*.segments.xml` `segment@nite:id` (string): unique AMI segment id.

`segments/*.segments.xml` `segment@channel` (integer-like string): AMI channel identifier for the segment file.

`segments/*.segments.xml` `segment@transcriber_start` (float seconds): segment start time from the transcriber annotation.

`segments/*.segments.xml` `segment@transcriber_end` (float seconds): segment end time from the transcriber annotation.

`segments/*.segments.xml` `nite:child@href` (string): reference to one word id or a contiguous range of word ids in the corresponding `words` file.

`dialogueActs/*.dialog-act.xml` root id (string): AMI document id for one meeting-speaker dialogue-act stream.

`dialogueActs/*.dialog-act.xml` `dact@nite:id` (string): unique dialogue-act id.

`dialogueActs/*.dialog-act.xml` `nite:pointer@role` (string): role of a dialogue-act ontology pointer.

`dialogueActs/*.dialog-act.xml` `nite:pointer@href` (string): reference to the dialogue-act ontology item.

`dialogueActs/*.dialog-act.xml` `nite:child@href` (string): reference to one word id or a contiguous range of word ids covered by the dialogue act.

`ami_public_manual_1.6.2/LICENCE.txt` (text): Creative Commons Attribution 4.0 license text bundled by AMI.

## Audio format

The imported AMI headset-mix files are WAV audio files sampled at 16 kHz. They are full source meeting recordings, not pre-extracted challenge clips.

## License

CC BY 4.0. The official AMI license page states that the AMI corpus and annotations are released under the Creative Commons Attribution 4.0 license agreement. The official AMI download page also states that the signals and transcription, and some annotations, are released under CC BY 4.0.

## Source

Official AMI Corpus page: https://groups.inf.ed.ac.uk/ami/corpus/

Official AMI license page: https://groups.inf.ed.ac.uk/ami/corpus/license.shtml

Official AMI download page: https://groups.inf.ed.ac.uk/ami/download/

Official AMI manual annotations: https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip

OpenSLR AMI mirror page checked for reference: https://www.openslr.org/16/

The OpenSLR SLR16 page is useful as a mirror/index for AMI acoustic data, but it displays an older modified BY-NC-SA license note and points readers to the AMI webpage for details. This dataset uses the official AMI pages above as the license source of record.

## Direct import URLs

```text
https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/ES2002a/audio/ES2002a.Mix-Headset.wav
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/ES2003a/audio/ES2003a.Mix-Headset.wav
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/ES2004a/audio/ES2004a.Mix-Headset.wav
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/IS1000a/audio/IS1000a.Mix-Headset.wav
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/TS3003a/audio/TS3003a.Mix-Headset.wav
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/EN2001a/audio/EN2001a.Mix-Headset.wav
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/IB4001/audio/IB4001.Mix-Headset.wav
https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/IN1001/audio/IN1001.Mix-Headset.wav
```

## Notes

* The raw files are source AMI artifacts, not pre-baked challenge clips or splits.
* The imported source files preserve full meeting audio and official manual timing annotations.
* The bounded source subset keeps the raw import size far below the platform cap while preserving real multi-party meeting speech.
