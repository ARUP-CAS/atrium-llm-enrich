"""tests/test_vendored_teitok_parity.py -- the TEITOK files vendored from atrium-nlp-enrich.

atrium-nlp-enrich writes TEITOK XML and owns the code that reads and converts it; this repo
only reads it. The files below are verbatim copies of the nlp-enrich files at the same paths.
Before this test, CONTRIBUTING.md claimed the copies were verbatim while nothing checked it:
``teitok_read.py`` had drifted in both directions (each copy had fixes the other lacked),
and a stale fork of the TEITOK *writer* (``api_util/teitok_alto.py``) lived on here with
tests of its own.

Each copy is pinned by the SHA-256 of the nlp-enrich file it was taken from (line endings
normalised to ``\\n``). A mismatch means a local edit to a vendored file -- make the change
in atrium-nlp-enrich instead -- or a re-vendor without updating the pins.

To re-vendor:

1. Copy the files from atrium-nlp-enrich (same relative paths).
2. Run ``python3 tests/test_vendored_teitok_parity.py`` and paste its output over
   ``VENDORED`` below.
3. Commit the copies and the new pins together.

When an atrium-nlp-enrich checkout sits next to this repo (``../atrium-nlp-enrich``),
the copies are also compared with it byte for byte. That check is skipped when the
checkout is absent (CI).
"""

import hashlib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
NLP_ENRICH = REPO_ROOT.parent / "atrium-nlp-enrich"

VENDORED = {
    "api_util/teitok_read.py": "9b8e952d5bc2e4039fc35c023702b65c7b6cf195a580c139d0ec8dd441f62024",
    "api_util/flexiconv_convert.py": "c01c8eddb97a6cc0ce92ab54a4eec52d86aba9c77e4e168713e898a1cd3ffa6f",
    "api_util/bbox_scale.py": "3bc5669f72bbabb63fb8c5e1e8d9bf9ad8ed920cf603102a25b5271b55b7ab3b",
    "requirements_flexiconv.txt": "b89e439836318f6322192f3cf658ea2f95741b015849b575ad8d8f32074580f8",
    "tests/test_flexiconv_convert.py": "3be49573d34861dcb8086cd1c11103d950f6f097de6b28011c05f87e66bb9c02",
    "tests/fixtures/teitok/flexiconv/alto.teitok.xml": "78a816383999f644e3c96834a2dc85e73f545c1672e94676b4190de607e0430a",
    "tests/fixtures/teitok/flexiconv/hocr.teitok.xml": "6269e0fc38b17bcc092c9bbd1c0980e6d4c6a4475b4f1d84207deb86cb0ad885",
    "tests/fixtures/teitok/flexiconv/md.teitok.xml": "fac1588e979eb0273938a584fe8446e1bc22f380908572372fc8092617a088e1",
    "tests/fixtures/teitok/flexiconv/page.teitok.xml": "b5749dfd7ee4317d62a6f5771b44479d202f5db3545a9dec0b741e2e03138190",
    "tests/fixtures/teitok/flexiconv/txt.teitok.xml": "178a152004ce337819e0ad0c08680a8b5d686911558d21ddef99e35ca9501e35",
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


@pytest.mark.parametrize("rel", sorted(VENDORED))
def test_vendored_copy_matches_its_pin(rel):
    assert _digest(REPO_ROOT / rel) == VENDORED[rel], (
        f"{rel} differs from the atrium-nlp-enrich copy it was vendored from -- change it in "
        "atrium-nlp-enrich and re-vendor (see this module's docstring)"
    )


@pytest.mark.parametrize("rel", sorted(VENDORED))
def test_vendored_copy_matches_a_sibling_nlp_enrich_checkout(rel):
    upstream = NLP_ENRICH / rel
    if not upstream.is_file():
        pytest.skip("no ../atrium-nlp-enrich checkout next to this repo")
    assert _digest(REPO_ROOT / rel) == _digest(upstream), f"{rel} drifted from atrium-nlp-enrich"


def test_the_writer_is_not_vendored():
    """Only nlp-enrich writes TEITOK. A second copy of the writer here was a stale fork (no
    shared parse, other ids, other doc-id derivation) exercised only by copies of nlp's tests."""
    assert not (REPO_ROOT / "api_util" / "teitok_alto.py").exists()


if __name__ == "__main__":
    for rel in sorted(VENDORED):
        print(f'    "{rel}": "{_digest(REPO_ROOT / rel)}",')
