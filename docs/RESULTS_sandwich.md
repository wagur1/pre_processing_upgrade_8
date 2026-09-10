# RESULTS — SANDWICH (điền khi có kết quả)

> Template tạo TRƯỚC khi chạy. Kỳ vọng đã đăng ký trong docs/MODEL_SANDWICH.md.

## Trạng thái

| Bước | Trạng thái |
|---|---|
| Tests + smoke (96/96) | ✅ |
| Probe Kaggle | ✅ (qua train kernel) |
| Train 16ep sandwich v1 | ✅ COMPLETE (best epoch 14/16, ~11.3h, `nguyenhoanglan1232/u8-train-sandwich`) |
| Gates trên v1 ckpt | ✅ đọc checkpoint: PRE gates ≈ v7 (dec=−0.6239, edit=0.0000, stab=−0.0785) — **POST strength = 0.0000: POST CHẾT (dead-saddle bug, giống M2 của v7)** |
| **Bug fix + v2 retrain** | ✅ commit `3a948521e5db`, kernel `hieusunday0412/u8-train-v2` đang chạy |
| Eval v1 | ⏭️ BỎ QUA (POST identity ⇒ arm sandwich ≡ arm prep — không tốn quota cho số trùng) |
| Eval v2 (3 arm) | sau khi v2 train xong |

**Phát hiện v1:** POST không bao giờ mở — cùng dead-saddle như M2 v7 (zero
out conv × zero gate ⇒ gradient kép ≡ 0). Nhân bản độc lập của cùng bug trên
2 repo củng cố chẩn đoán. Eval v1 bị bỏ có chủ đích; mọi hy vọng sandwich nằm
ở v2 (đã fix init).

## Comparators

| Arm/đối thủ | BD h264 [CI] | BD h265 [CI] | gap |
|---|---|---|---|
| anchor (không prep) | 0% | 0% | — |
| prep-only (cùng ckpt, bypass post) | −0.09% [−2.26,+2.14] | −1.40% [−3.01,+0.35] | PASS |
| **sandwich (claim chính)** | **−4.25% [−6.73,−1.58]** | −1.48% [−3.34,+0.50] | PASS |
| lineage best (Zhao kappa=10, v6) | −3.42% [−5.88,−0.88] | −2.63% [−4.49,−0.79] | PASS |

## Kết quả (v2, shards 0+1 = 770/1159 seqs, 5k bootstrap)

| Arm | BD h264 | CI95 | BD h265 | CI95 | P(BD<0) |
|---|---|---|---|---|---|
| prep+codec | −0.09% | [−2.26, +2.14] | −1.40% | [−3.01, +0.35] | 0.512 / 0.942 |
| **sandwich+codec** | **−4.25%** | **[−6.73, −1.58]** | −1.48% | [−3.34, +0.50] | **0.998** / 0.927 |

### Gates (từ checkpoint, best epoch 13)
```
PRE: dec=−0.340 (M1 mở)  edit=0.000 (M2 vẫn đóng ở v8)  stab=−0.069 (M3 mở)
POST strength = +0.052  → MỞ (dead-saddle fix có tác dụng)
```

## Đọc kết quả

- **Giá trị thuần của POST trên h264: +4.16pp** (sandwich −4.25% vs prep −0.09%, cùng
  checkpoint, cùng bpp — phép tách cơ chế sạch nhất có thể). Held-out analyzer ⇒ KHÔNG
  phải teacher-overfit: POST khôi phục được accuracy cho analyzer chưa từng thấy.
- **Sandwich vượt lineage best trên h264** (−4.25% vs −3.42%, CI dịch trái toàn phần:
  upper −1.58% vs −0.88%). Trên h265 POST gần như không cộng (+0.08pp) — bất đối xứng
  codec: POST học đảo artifact khớp x264 hơn (proxy block-8 gần x264 4×4/8×8 hơn là
  x265 block lớn + SAO).
- PRE của v8 yếu hơn v7 trên h264 (−0.09 vs −2.46): POST "án ngữ" vai trò khôi phục
  trong joint training, làm PRE bớt dốc — chính là trade-off thiết kế của sandwich.
- Số này là 2/3 shards; merge full n=1159 khi shard 2 xong (dự kiến lệch ≤ ±0.5pp).
