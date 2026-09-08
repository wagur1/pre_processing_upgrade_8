# RESULTS — SANDWICH (điền khi có kết quả)

> Template tạo TRƯỚC khi chạy. Kỳ vọng đã đăng ký trong docs/MODEL_SANDWICH.md.

## Trạng thái

| Bước | Trạng thái |
|---|---|
| Tests + smoke (95/95) | ☐ |
| Probe Kaggle | ☐ |
| Train 16ep sandwich | ☐ |
| Gates G1–G6 | ☐ |
| Eval sharded 3 arm | ☐ |
| Merge + CI + gap rule | ☐ |

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
