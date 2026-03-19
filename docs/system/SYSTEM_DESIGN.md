## Phân Chia Trách Nhiệm

| | BE1 — LPR | BE2 — Main |
|--|-----------|------------|
| Trigger | Điện thoại gửi ảnh | Dashboard, Admin |
| MQTT subscribe | `sensors/gate/*` | `sensors/slot/#`, `heartbeat/#` |
| MQTT publish | `command/gate/*` | — |
| DB owns | `parking_sessions` | `parking_slots`, `pricing_config`, `users` |
| Logic | Nhận diện AI + tính tiền | Auth, thống kê, cấu hình |

> 2 BE không gọi nhau. 1 cái crash, cái kia vẫn sống.

---

## Luồng Xe Vào

```
1. ESP32 IR phát hiện xe
2. ESP32 MQTT publish → sensors/gate/entry { v:1 } → BE1
3. ESP32 USB Serial → Điện thoại chụp ảnh
4. Điện thoại HTTP POST ảnh → BE1 /recognize
5. BE1 nhận diện biển số
6. BE1 INSERT parking_sessions { plate, entry_time, status: active }
7. BE1 MQTT publish → command/gate/entry { action: "open" }
8. ESP32 nhận lệnh → mở barrier
9. [async] BE1 upload ảnh → Storage → UPDATE parking_sessions
```

---

## Luồng Xe Ra

```
1. ESP32 IR phát hiện xe
2. ESP32 MQTT publish → sensors/gate/exit { v:1 } → BE1
3. ESP32 USB Serial → Điện thoại chụp ảnh
4. Điện thoại HTTP POST ảnh → BE1 /recognize
5. BE1 nhận diện biển số
6. BE1 query parking_sessions (tìm session active)
7. BE1 tính tiền theo pricing_config
8. BE1 UPDATE parking_sessions { exit_time, fee, status: completed }
9. BE1 MQTT publish → command/gate/exit { action: "open" }
10. ESP32 nhận lệnh → mở barrier
11. [async] BE1 upload ảnh → Storage → UPDATE parking_sessions
```

---

## Luồng Cảm Biến Slot

```
1. ESP32 IR phát hiện thay đổi ô đỗ
2. MQTT publish → sensors/slot/slot_001 { v:1 }
3. BE2 nhận → UPDATE parking_slots { status: occupied }
4. Supabase Realtime → Dashboard cập nhật sơ đồ
```

---

## Barrier Strategy

> Ưu tiên xe không bị kẹt hơn dữ liệu hoàn hảo.

| Tình huống | Xử lý |
|-----------|-------|
| Nhận diện OK, DB OK | Mở barrier |
| Nhận diện OK, DB lỗi | Mở barrier + retry background |
| Không nhận diện được | Mở barrier, plate = `UNKNOWN_{timestamp}` |
| BE1 timeout (5s) | Không mở + báo nhân viên |

<p align="center">
  <a href="../PROBLEM_DEFINITION.md">← Định nghĩa bài toán</a> •
  <a href="../MVP_SCOPE.md">Phạm vi MVP →</a>
</p>
