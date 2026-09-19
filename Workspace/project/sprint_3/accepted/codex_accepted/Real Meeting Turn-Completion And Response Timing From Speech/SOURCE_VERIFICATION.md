# Source Verification

Checked on 2026-07-02.

* Official corpus page: https://groups.inf.ed.ac.uk/ami/corpus/ describes the AMI Meeting Corpus as about 100 hours of multi-modal meeting recordings with close-talking and far-field microphones, video, transcription, and annotations, and states that signals, transcription, and some annotations are public under CC BY 4.0.
* Official license page: https://groups.inf.ed.ac.uk/ami/corpus/license.shtml states that the AMI corpus and annotations are released under Creative Commons Attribution 4.0, also called CC BY 4.0.
* Official download page: https://groups.inf.ed.ac.uk/ami/download/ provides direct manual annotation downloads and per-meeting signal download scripts; the manual annotation entry says the license was altered to CC BY 4.0.
* OpenSLR page: https://www.openslr.org/16/ mirrors AMI acoustic data and metadata but still shows an older modified BY-NC-SA license note while pointing users back to the AMI webpage for details.

This challenge uses the official AMI page and license page as the source of record. The platform data files should be imported directly from the official AMI URLs listed in `URL_IMPORT_LIST.txt`; local `raw_data/` mirrors that source-file layout for testing. All challenge-specific clipping, label derivation, splitting, and anonymization happens in `prepare.py`.
