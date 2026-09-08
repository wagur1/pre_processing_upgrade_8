# pre_processing_upgrade_8 — SANDWICH: PRE + POST quanh codec đóng băng

**VCM (Video Coding for Machines) với bộ lọc kép: PRE cắt bit trước encode,
POST khôi phục sau decode — codec chuẩn (x264 / x265) và analyzer giữ nguyên
hoàn toàn.**

Pre-only mua accuracy đúng theo tỉ giá của anchor. Sandwich thêm nửa POST
(restoration filter sau decode, trước analyzer) với **chi phí bit bằng không**:
accuracy codec phá đi được mua lại phía decoder, cho phép PRE cắt bit mạnh hơn.

```
            PRE (UP-VCM)                      POST (mới)
 x ─► pre(x) ─► x264/x265 (đóng băng) ─► decode x̂ ─► post(x̂) ─► analyzer
     ~44k params                        ~577k params, 0 bit

Claim: BD-Rate(sandwich+codec vs codec) trên trục accuracy analyzer held-out.
```

## Kiến trúc (docs/MODEL_SANDWICH.md)

| Nửa | Thành phần |
|---|---|
| **PRE** (~44k) | nguyên UP-VCM: S importance head (distill teacher+DINOv2, tự chủ khi deploy) + M1 background decimation + M2 ROI editor FiLM(QP) + M3 ổn định nền thời gian |
| **POST** (~577k) | restoration UNet 3 tầng + FiLM(QP), gate `post_strength` zero-init → identity lúc khởi tạo; input chỉ là clip đã decode |

- Huấn luyện joint end-to-end qua proxy codec yuv420: loss trên `post(codec(pre(x)))`
- Stage-2 STE: codec thật trong vòng lặp → POST học đảo artifact x264/x265 thật
- Checkpoint PRE của v7 strict-load (`load_pre_state`) — warm-start được test

## Eval — 3 arm cùng checkpoint (tách cơ chế)

| Arm | Đường | Báo cáo |
|---|---|---|
| anchor | codec(x) → analyzer | baseline |
| prep+codec | pre(x) → codec → analyzer (bypass post) | đóng góp PRE |
| **sandwich+codec** | pre(x) → codec → **post** → analyzer | **claim chính** |

Protocol chuẩn: test set 1159 clip (fingerprint `30f083f8520a`), analyzer
held-out `r2plus1d_18`, x264+x265 preset medium QP {30–50}, per-sequence →
merge → BD-Rate + bootstrap CI 95% + gap rule (`prep/sandwich − anchor ≥ −0.05`
mọi QP, cả hai codec).

## Pipeline

```bash
# local
pytest -q                                          # 95 tests
python ops/smoke_local.py configs/sandwich_ar.yaml # full pipeline, dữ liệu giả

# Kaggle (source ops/kaggle_env.sh <account>; pin T4!)
source ops/kaggle_env.sh wagur124705
python ops/push_kernel.py probe  --commit <sha> --no-gpu
python ops/push_kernel.py train  --commit <sha> --config configs/sandwich_ar.yaml \
    --accelerator NvidiaTeslaT4
python ops/gates_sandwich.py --ckpt <preprocessor.pth> --index <index.json>
#  G1–G4 (PRE validity) + G5 POST opened + G6 POST restores
python ops/push_kernel.py eval   --commit <sha> --shard-idx N --num-shards 3 \
    --train-kernel <account>/u8-train-sandwich --accelerator NvidiaTeslaT4
python ops/merge_eval.py <shard0> <shard1> <shard2> --out outputs/eval_sandwich_merged
```

## Cấu trúc repo

```
configs/sandwich_ar.yaml      # config chính
src/models/sandwich.py        # SandwichPreprocessor (PRE wrap + POST UNet)
src/models/upvcm.py           # PRE half (UP-VCM)
src/models/dino_saliency.py   # DINOv2 energy (train-time anchor cho S)
src/engine.py                 # train/eval: post_restore sau codec, 3-arm eval
ops/gates_sandwich.py         # 6 gates (PRE validity + POST mechanism)
ops/                          # Kaggle ops (parameterized theo config)
docs/MODEL_SANDWICH.md        # thiết kế + kỳ vọng đăng ký trước
docs/RESULTS_sandwich.md      # kết quả
tests/                        # 95 tests
```

## Tham chiếu

- Sandwiched Compression (arXiv:2402.05887) — thiết kế pre/post với codec đóng băng (metric con người)
- DINOv2 (Oquab et al., 2023); RPP (arXiv:2301.10455); FiLM (Perez et al. 2018)
- Lu et al. (arXiv:2206.05650) — forward-real-codec STE (−20.3% vs −14.6%)
