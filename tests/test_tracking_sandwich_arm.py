"""Checks for the tracking-eval sandwich arm (engine._post_chunked + gate).

2026-09-12: _evaluate_tracking gained the third arm (sandwich+codec — POST
restores the decoded clip at zero bit cost), mirroring the classification
eval. These checks pin the chunking helper and the arm gate without needing
ffmpeg or GOT-10k data.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.engine import _post_chunked
from src.models.sandwich import SandwichPreprocessor
from src.models.upvcm import UPVCMPreprocessor


def _tiny_sandwich() -> SandwichPreprocessor:
    return SandwichPreprocessor(s_ch=4, editor_ch=4, cond_dim=1, post_base=4)


def test_post_chunked_preserves_length_and_order() -> None:
    pre = _tiny_sandwich()
    T = 12
    clip = torch.rand(1, 3, T, 32, 32)
    out = _post_chunked(pre, clip, chunk=5, cond=None)
    assert out.shape == clip.shape, "chunked POST must rebuild the full T"
    # zero-init gate -> identity: chunk boundaries must not introduce seams
    assert torch.allclose(out, clip, atol=1e-6), "identity POST must be seamless across chunks"


def test_post_chunked_chunk_equals_full_length() -> None:
    pre = _tiny_sandwich()
    clip = torch.rand(1, 3, 7, 32, 32)
    out = _post_chunked(pre, clip, chunk=7, cond=None)
    assert torch.allclose(out, clip, atol=1e-6)


def test_sandwich_arm_gate_matches_model_capability() -> None:
    has_post = hasattr(_tiny_sandwich(), "post_restore")
    assert has_post, "SandwichPreprocessor must expose post_restore for the tracking sandwich arm"
    assert not hasattr(UPVCMPreprocessor(s_ch=4, editor_ch=4), "post_restore"), (
        "a PRE-only model must not pass the has_post gate (prep-only 2-arm eval)"
    )


def test_post_restore_bypass_returns_input() -> None:
    pre = _tiny_sandwich()
    pre.bypass_post = True
    clip = torch.rand(1, 3, 4, 32, 32)
    assert torch.allclose(pre.post_restore(clip, None), clip, atol=1e-7)


if __name__ == "__main__":
    test_post_chunked_preserves_length_and_order()
    test_post_chunked_chunk_equals_full_length()
    test_sandwich_arm_gate_matches_model_capability()
    test_post_restore_bypass_returns_input()
    print("tracking sandwich-arm self-checks passed")
