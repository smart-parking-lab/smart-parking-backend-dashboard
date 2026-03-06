# 🔀 Quy Trình Git & Luật Push Code

> Quy tắc sử dụng Git cho team 5 người, phân chia theo module.

---

## 📌 Nguyên Tắc Vàng

```
⚠️  KHÔNG BAO GIỜ push trực tiếp lên main
⚠️  KHÔNG BAO GIỜ force push lên branch của người khác
⚠️  LUÔN tạo Pull Request để merge vào main
```

---

## 🌿 Branching Strategy

```
main (protected)
 │
 ├── feature/parking-core/slot-manager       ← Tùng
 ├── feature/parking-core/pricing-engine     ← Tùng
 ├── feature/user/auth                       ← Hùng
 ├── feature/user/booking                    ← Chiến
 ├── feature/payment/billing                 ← Chiến
 ├── feature/data-acquisition/mqtt-listener  ← Chính
 ├── fix/sensor/heartbeat-timeout            ← Chính
 └── docs/getting-started                    ← Ai đó
```

### Quy Tắc Đặt Tên Branch

| Pattern | Khi nào dùng | Ví dụ |
|---------|-------------|-------|
| `feature/<module>/<mô-tả>` | Thêm tính năng mới | `feature/payment/vnpay-integration` |
| `fix/<module>/<mô-tả>` | Sửa bug | `fix/sensor/mqtt-reconnect` |
| `docs/<mô-tả>` | Cập nhật tài liệu | `docs/api-endpoints` |
| `refactor/<module>/<mô-tả>` | Refactor code | `refactor/auth/jwt-middleware` |

---

## 💬 Commit Message Convention

### Format

```
<emoji> <type>(<scope>): <mô tả ngắn>

[body - tùy chọn]
```

### Bảng Emoji + Type

| Emoji | Type | Khi nào dùng |
|-------|------|-------------|
| ✨ | `feat` | Thêm tính năng mới |
| 🐛 | `fix` | Sửa bug |
| 📝 | `docs` | Cập nhật tài liệu |
| ♻️ | `refactor` | Refactor (không đổi logic) |
| 🧪 | `test` | Thêm/sửa test |
| 🔧 | `chore` | Config, dependencies, CI |
| 🚀 | `deploy` | Deploy, Dockerfile |
| 🗑️ | `remove` | Xóa code/file không dùng |
| 🎨 | `style` | Format code (không đổi logic) |
| ⚡ | `perf` | Cải thiện performance |
| 🔒 | `security` | Fix lỗ hổng bảo mật |

### Ví Dụ Cụ Thể

<details>
<summary>📌 Click để xem ví dụ chi tiết</summary>

#### Khi thêm tính năng mới
```
✨ feat(booking): thêm API đặt chỗ trước

- Thêm endpoint POST /api/v1/bookings
- Thêm BookingCreate, BookingResponse schemas
- Thêm BookingService với logic giữ chỗ 15 phút
```

#### Khi sửa bug
```
🐛 fix(sensor): sửa lỗi parse MQTT payload khi thiếu field timestamp

Cảm biến firmware v1.2 không gửi field timestamp,
gây crash signal_processor. Thêm giá trị mặc định.
```

#### Khi cập nhật docs
```
📝 docs: thêm hướng dẫn cài đặt UV trên Windows
```

#### Khi refactor
```
♻️ refactor(auth): tách JWT verify logic ra core/security.py
```

#### Khi thêm test
```
🧪 test(payment): thêm unit test cho PricingEngine.calculate()
```

#### Khi thay đổi config
```
🔧 chore: thêm ruff và ty vào dev dependencies
```

#### Khi xóa code cũ
```
🗑️ remove(api): xóa endpoint GET /api/v1/test không dùng
```

</details>

---

## 🔄 Quy Trình Làm Việc

### Bước 1: Tạo Branch Mới

```bash
# Cập nhật main mới nhất
git checkout main
git pull origin main

# Tạo branch mới
git checkout -b feature/parking-core/slot-manager
```

### Bước 2: Code & Commit

```bash
# Kiểm tra thay đổi
git status

# Stage files
git add src/app/services/slot_manager.py
git add src/app/schemas/slot.py

# Commit với emoji
git commit -m "✨ feat(parking-core): thêm SlotManager service"
```

> [!TIP]
> Commit thường xuyên, mỗi commit nên là **1 thay đổi logic hoàn chỉnh**.
> Không nên gom hết vào 1 commit khổng lồ.

### Bước 3: Push & Tạo Pull Request

```bash
# Push branch lên remote
git push origin feature/parking-core/slot-manager
```

Sau đó vào **GitHub** → tạo **Pull Request** vào `main`:

- **Title**: Copy commit message chính (ví dụ: `✨ feat(parking-core): thêm SlotManager service`)
- **Description**: Mô tả ngắn những gì đã làm
- **Reviewer**: Tag ít nhất **1 người** khác review

### Bước 4: Review & Merge

```
📋 Checklist review:
  □ Code chạy được, không lỗi cú pháp
  □ Đã có xử lý lỗi (try/except, raise exception)
  □ Đã có xử lý trường hợp rỗng
  □ Tên file, class, function đúng quy ước
  □ Import tuyệt đối (from app.xxx)
  □ Không commit file .env, __pycache__, .venv
```

- Dùng **Squash and Merge** để giữ history sạch
- Sau khi merge, **xóa branch** trên remote

---

## 👥 Phân Chia Module

| Module | Owner | Folder chính |
|--------|-------|-------------|
| Data Acquisition | Chính | `data_acquisition/`, `api/v1/sensors.py` |
| Parking Core | Tùng | `services/slot_manager.py`, `services/pricing_engine.py`, `api/v1/slots.py` |
| User & Reservation | Hùng + Chiến | `services/auth_service.py`, `services/booking_service.py`, `api/v1/auth.py`, `api/v1/bookings.py` |
| Payment | Chiến | `services/billing_service.py`, `services/payment_service.py`, `api/v1/payments.py` |
| UI & Analytics | Chính | `services/report_service.py`, `api/v1/reports.py` |
| Core & Utils | Chính | `core/`, `utils/` |

> [!IMPORTANT]
> Nếu cần sửa file trong module **không phải của mình**, hãy **tag owner** để review trong PR.

---

## ⚡ Xử Lý Conflict

```bash
# Khi có conflict, cập nhật main mới nhất
git checkout main
git pull origin main

# Quay lại branch của mình và rebase
git checkout feature/parking-core/slot-manager
git rebase main

# Giải quyết conflict trong editor
# Sau khi fix xong:
git add .
git rebase --continue

# Push lại (cần force vì đã rebase)
git push origin feature/parking-core/slot-manager --force-with-lease
```

> [!CAUTION]
> Chỉ dùng `--force-with-lease` (KHÔNG dùng `--force`). Và chỉ force push **branch của mình**, **KHÔNG BAO GIỜ** force push `main`.

---

## 🛡️ Bảo Vệ Branch `main`

Cần cấu hình trên GitHub:

1. Vào **Settings** → **Branches** → **Add rule**
2. Branch name pattern: `main`
3. Bật:
   - ☑️ Require a pull request before merging
   - ☑️ Require approvals (1 người)
   - ☑️ Do not allow bypassing the above settings

---

## 📊 Tóm Tắt Nhanh

```
                    ┌──────────────────┐
                    │   main (protected)│
                    └────────▲─────────┘
                             │ Squash Merge (qua PR)
                    ┌────────┴─────────┐
                    │  Pull Request     │
                    │  + Code Review    │
                    └────────▲─────────┘
                             │ push
              ┌──────────────┴──────────────┐
              │  feature/module/tên-feature  │
              └──────────────────────────────┘
                       ↑ checkout -b
                    ┌──────┐
                    │ main │
                    └──────┘
```

---

<p align="center">
  <a href="GETTING_STARTED.md">Tiếp: 🚀 Hướng dẫn khởi động →</a>
</p>
