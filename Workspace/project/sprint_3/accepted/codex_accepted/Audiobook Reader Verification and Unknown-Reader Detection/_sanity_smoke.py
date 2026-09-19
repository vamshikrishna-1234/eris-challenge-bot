from __future__ import annotations

import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf

from grade import InvalidSubmissionError, grade
from prepare import prepare


SR = 16000


def _voice(path: Path, speaker: str, idx: int, subset: str) -> None:
    seed = int(speaker) * 1000 + idx
    rng = np.random.default_rng(seed)
    seconds = 1.4 + 0.11 * (idx % 6)
    t = np.arange(int(seconds * SR), dtype=np.float32) / SR
    base_freq = 115 + (int(speaker) % 70) + 5 * (idx % 4)
    signal = 0.40 * np.sin(2 * np.pi * base_freq * t)
    signal += 0.16 * np.sin(2 * np.pi * (2.01 * base_freq) * t + 0.2)
    signal += 0.08 * np.sin(2 * np.pi * (3.03 * base_freq) * t + 0.7)
    envelope = 0.78 + 0.18 * np.sin(2 * np.pi * (2.0 + (int(speaker) % 5)) * t)
    signal *= envelope
    signal += 0.006 * rng.normal(size=t.size)
    if subset == "dev-clean-2":
        signal += 0.010 * rng.normal(size=t.size)
    signal = signal / max(float(np.max(np.abs(signal))), 1e-6) * 0.85
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, signal.astype(np.float32), SR, format="FLAC")


def _write_split(librispeech_root: Path, subset: str, speakers: list[str], start_chapter: int) -> None:
    for speaker in speakers:
        chapter = str(start_chapter + int(speaker) % 1000)
        chapter_dir = librispeech_root / subset / speaker / chapter
        lines = []
        for idx in range(14):
            utt = f"{speaker}-{chapter}-{idx:04d}"
            _voice(chapter_dir / f"{utt}.flac", speaker, idx, subset)
            lines.append(f"{utt} THIS IS A REAL SPEECH FIXTURE UTTERANCE NUMBER {idx} FROM READER {speaker}")
        (chapter_dir / f"{speaker}-{chapter}.trans.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _make_fixture(raw: Path, wrapped: bool) -> None:
    root = raw / "LibriSpeech" if wrapped else raw
    root.mkdir(parents=True, exist_ok=True)
    known = ["101", "102", "103", "104", "105", "106"]
    unknown = ["201", "202", "203", "204"]
    speakers = []
    for speaker in known + unknown:
        sex = "M" if int(speaker) % 2 == 0 else "F"
        speakers.append(f"{speaker} | {sex} | train | 1.0 | Fixture Reader {speaker}")
    (root / "SPEAKERS.TXT").write_text(";ID | SEX | SUBSET | MINUTES | NAME\n" + "\n".join(speakers) + "\n", encoding="utf-8")
    _write_split(root, "train-clean-5", known, 7000)
    _write_split(root, "dev-clean-2", unknown, 8000)


def _assert_score(name: str, value: float, lo: float, hi: float) -> None:
    if not (lo <= value <= hi):
        raise AssertionError(f"{name} score {value} outside [{lo}, {hi}]")


def _assert_invalid(name: str, submission: pd.DataFrame, answers: pd.DataFrame) -> None:
    try:
        grade(submission, answers)
    except InvalidSubmissionError:
        return
    raise AssertionError(f"{name} should raise InvalidSubmissionError")


def _run_case(case_name: str, wrapped: bool) -> None:
    with tempfile.TemporaryDirectory(prefix=f"real_audiobook_provenance_{case_name}_") as td:
        root = Path(td)
        raw = root / "raw"
        public = root / "public"
        private = root / "private"
        _make_fixture(raw, wrapped=wrapped)
        prepare(raw, public, private, max_rows=120, allow_tiny_fixture=True)

        train = pd.read_csv(public / "train.csv")
        test = pd.read_csv(public / "test.csv")
        answers = pd.read_csv(private / "answers.csv")
        sample = pd.read_csv(public / "sample_submission.csv")
        perfect = answers[["id", "verdict_json"]].copy()

        perfect_score = grade(perfect, answers)
        sample_score = grade(sample, answers)
        _assert_score("perfect", perfect_score, 1.0, 1.0)
        _assert_score("sample", sample_score, 0.12, 0.50)
        if grade(sample, answers.set_index("id", drop=False)) != sample_score:
            raise AssertionError("grader should be stable when answers are indexed by id")
        if grade(perfect, answers.set_index("id", drop=False)) != perfect_score:
            raise AssertionError("perfect score should survive answers indexed by id")

        wrong_cols = sample[["verdict_json", "id"]]
        dup = pd.concat([sample.iloc[:1], sample.iloc[:1], sample.iloc[2:]], ignore_index=True)
        missing = sample.iloc[:-1].copy()
        bad_conf = sample.copy()
        obj = json.loads(bad_conf.loc[0, "verdict_json"])
        obj["confidence"] = 2.0
        bad_conf.loc[0, "verdict_json"] = json.dumps(obj)
        malformed = sample.copy()
        malformed.loc[0, "verdict_json"] = "{not-json"
        all_malformed = sample.copy()
        all_malformed["verdict_json"] = "{not-json"

        _assert_invalid("wrong columns", wrong_cols, answers)
        _assert_invalid("duplicate ids", dup, answers)
        _assert_invalid("missing ids", missing, answers)
        _assert_invalid("bad confidence", bad_conf, answers)
        malformed_score = grade(malformed, answers)
        if not (0.0 <= malformed_score < perfect_score):
            raise AssertionError("malformed JSON row should degrade without crashing")
        all_malformed_score = grade(all_malformed, answers)
        _assert_score("all malformed", all_malformed_score, 0.0, 0.0)

        assert set(train.columns) == {"id", "audio_path", "duration_sec", "utterance_length_bucket", "verdict_json"}
        assert set(test.columns) == {"id", "audio_path", "duration_sec", "utterance_length_bucket"}
        assert "UNKNOWN" in set(answers["provenance"])
        assert "UNKNOWN" not in {json.loads(v)["provenance"] for v in train["verdict_json"]}
        assert not set(train["id"]) & set(test["id"])
        for rel in pd.concat([train["audio_path"], test["audio_path"]]).astype(str):
            assert (public / rel).exists(), rel
            low = rel.lower()
            assert not any(tok in low for tok in ["librispeech", "train-clean", "dev-clean", "speaker", "chapter"]), rel

        print(f"OK smoke {case_name}: train={len(train)} test={len(test)}")
        print(f"sample_score={sample_score:.6f}")
        print(f"perfect_score={perfect_score:.6f}")
        print(f"malformed_row_score={malformed_score:.6f}")
        print(f"all_malformed_score={all_malformed_score:.6f}")
        print("test provenance counts:", answers["provenance"].value_counts().to_dict())
        print("hidden source counts:", answers["source_split"].value_counts().to_dict())


def main() -> None:
    _run_case("wrapped_librispeech", wrapped=True)
    _run_case("platform_extracted", wrapped=False)


if __name__ == "__main__":
    main()
