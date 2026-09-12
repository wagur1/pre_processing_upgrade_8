# Data guide for report/PPT builders (2026-09-11/12 campaign)

All numbers below are BD-Rate % (negative = bitrate savings), bootstrap CI 95%, full test sets.
Protocol: x264/x265 frozen, preset medium, QP 30-50; analyzer r2plus1d_18 held-out unless stated;
gap rule ≥ −0.05 top-1 at every QP. Raw per-clip points live in the local harvest stash; every
committed artifact below is reproducible from `ops/merge_eval.py`.

## Headline (confirmatory, n=11,724 never-used clips) — for the title slide

| Model | h264 [CI] | h265 [CI] | File |
|---|---|---|---|
| **E4 SANDWICH** (PRE 44k + POST 2.3M) | **−4.61 [−5.54,−3.68]** | **−3.89 [−4.52,−3.27]** | `outputs/eval_e4_confirmatory/merged_results.json` |
| v9-b DualCodec | −4.59 [−5.55,−3.63] | −3.18 [−3.80,−2.56] | (repo pre_processing_upgrade_9) `outputs/eval_v9b_confirmatory/merged_results.json` |

P(BD<0)=1.000 everywhere; gap rule PASS. No selection bias (audit #4).

## Transfer-gap 2x2 (figure: the analyzer-agnostic story)

Rows = same checkpoint evaluated with 2 analyzers (n=1159):

| Arm | on-teacher | held-out |
|---|---|---|
| Zhao slowfast (re-impl, matched compute) | +34.30 / +13.44 (gap FAIL) | +39.96 / +17.85 |
| Zhao slowonly | −3.57 (ns) / +2.49 | +3.27 / +1.12 |
| **E4 (ours)** | **−5.71 / −4.22** | **−5.71 / −4.22** |

Files: `outputs/eval_e4_onteacher/merged_results.json` (ours), `outputs/eval_zhao_*/merged_results.json`
(held-out), baseline repo `outputs/eval_zhao_*_onteacher/merged_results.json`.
Takeaway: Zhao collapses even on its own teacher → codec-proxy mismatch dominates; E4 is identical
across analyzers (multi-teacher distillation + real codecs in the loop).

## Ablations (n=1159, exploratory)

| Config | h264 | h265 | File |
|---|---|---|---|
| E4 (canonical) | −5.71 | −4.22 | `outputs/eval_e4_full/merged_results.json` |
| H1 PRE-swap | −4.13 | −3.19 | `outputs/eval_h1/merged_results.json` (falsified) |
| H3 STE calib | −3.96 | −4.00 | `outputs/eval_h3_ste/merged_results.json` (falsified) |
| E2 frank-STE | −5.89 | −2.79 | `outputs/eval_e2_reeval/merged_results.json` (re-confirmed, valid CI) |

## Per-sequence data (for histograms / best-worst clips / per-class)

`outputs/eval_*/per_sequence_bd.csv` — columns: `sequence_id,class,bd_h264_prep,bd_h264_sandwich,bd_h265_prep,bd_h265_sandwich`.
~60-65% of clips yield a finite 5-point per-clip BD fit (rest have degenerate anchor curves → None).
Available for: e4_confirmatory (11,724 clips), e4_onteacher, h1, h3_ste, e2_reeval, zhao_slowfast,
zhao_slowonly (v8 repo); v9b_confirmatory (v9 repo); zhao_*_onteacher (baseline repo, prep-only —
Zhao's method has no sandwich arm).

## Curves (for rate-accuracy figures)

`merged_results.json` `curves` field: per-codec dataset-level (bpp, top-1) at QP 30-50 for
anchor/prep/sandwich — plot-ready.

## Scale story (params → BD, from lineage)

POST 0 (pre-only) −2.46/−0.78 → 577k −4.45/−2.05 → 2.3M −5.71/−4.22 (monotone; not saturated).
