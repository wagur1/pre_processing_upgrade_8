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
| prep-only (cùng ckpt, bypass post) | | | |
| **sandwich (claim chính)** | | | |
| (tham chiếu ngoài instrument) v7 UP-VCM | | | |

## Kết quả

| Arm | BD h264 | CI95 | BD h265 | CI95 | P(BD<0) | gap |
|---|---|---|---|---|---|---|
| prep+codec | | | | | | |
| sandwich+codec | | | | | | |

### Gates
```
G1 PRE dec/edit/stab: ____   G2 PRE RMS: ____
G3 PRE W: mean ____ std ____  G4 purity: ____
G5 POST strength: ____        G6 RMS reduction: ____%
```

## Đọc kết quả (viết sau khi có số)

- Sandwich vs prep-only (cùng checkpoint, cùng bpp): chênh lệch = giá trị thuần của POST.
- Kiểm teacher-overfit: nếu gain sandwich biến mất trên held-out → "post overfits teacher", báo trung thực.
- Gap rule ở mọi QP; dung sai ±1pp cho mọi so sánh cùng instrument.
