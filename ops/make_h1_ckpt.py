"""H1: assemble 'best-of-everything' — PRE from v7-v1 + POST from E4 BIG-POST.

Evidence chain (all full-n, valid bootstrap):
  E4 BIG-POST  : PRE(weak −0.95) + POST(2.3M)  -> h264 −5.71 / h265 −4.22
  frankenstein : PRE-v1(−2.46)    + POST(577k)  -> h264 −4.82 / h265 −2.38
  v9-b         : per-codec PRE    + POST(577k)  -> h264 −5.89 / h265 −3.56

The one untested corner of the 2x2: PRE-v1 + BIG-POST. If the components
combine as they did everywhere else (additivity held in 3/4 assemblies),
this should land around h264 −6.5…−7 / h265 −4.5…−5 — the campaign's shot at
the −8 region when later combined with STE (H3).

Assembly is a plain SandwichPreprocessor state (same arch as E4 — eval works
unchanged): PRE weights replaced by v1's, POST trunk + gate from E4.
"""
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.models.sandwich import SandwichPreprocessor  # noqa: E402


def main():
    v1_path = "/tmp/v1_ckpt/pre_processing_upgrade_7/outputs/upvcm/checkpoints/preprocessor.pth"
    e4_path = "/tmp/e4_out/pre_processing_upgrade_8/outputs/sandwich/checkpoints/preprocessor.pth"
    out_path = "outputs/h1_bestof.pth"

    v1 = torch.load(v1_path, map_location="cpu")
    e4 = torch.load(e4_path, map_location="cpu")

    m = SandwichPreprocessor(post_base=64)
    # E4 skeleton first (POST + cfg), then v1 PRE overwrites (order matters)
    sd = e4["model"]
    m.load_state_dict(sd, strict=True)
    m.pre.load_state_dict(v1["model"], strict=True)

    ck = dict(e4)  # keep cfg (post_base=64, arch=sandwich)
    ck["model"] = m.state_dict()
    ck["epoch"], ck["global_step"], ck["best_val"], ck["no_improve"] = 0, 0, None, 0
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(ck, out_path)
    ms = ck["model"]
    print(f"saved {out_path}")
    print(f"  PRE (v1): dec={ms['pre.dec_strength'].item():+.4f} "
          f"edit={ms['pre.edit_strength'].item():+.4f} "
          f"stab={ms['pre.stab_strength'].item():+.4f}")
    print(f"  POST (E4 2.3M): strength={ms['post_strength'].item():+.4f}")
    n = sum(v.numel() for v in ms.values())
    print(f"  total params: {n:,}")


if __name__ == "__main__":
    main()
