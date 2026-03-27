# System Design — Smart Parking

## Thiết Bị

| Thiết bị | Số lượng | Vai trò |
|----------|----------|---------|
| ESP32 (CP2102) | 1 | 2 IR cổng + 4 IR slot + 2 servo barrier |
| Điện thoại | 1 | Server expose API `/capture` → chụp ảnh trả về BE1 |

---

## Kiến Trúc

```
ESP32 ──MQTT──► Broker ──► BE1 LPR ──► Supabase
                               ▲
                        HTTP /capture
                               │
                          Điện thoại

ESP32 ◄──MQTT── Broker ◄── BE1 LPR   (lệnh mở barrier + thông báo phí)

ESP32 ──MQTT──► Broker ──► BE2 Main ──► Supabase ──Realtime──► Dashboard
```

---

## Phân Chia Trách Nhiệm

| | BE1 — LPR | BE2 — Main |
|--|-----------|------------|
| MQTT subscribe | `sensors/gate/+` · `parking/payment_status` | `sensors/slot/#` · `heartbeat/#` |
| MQTT publish | `command/gate/+` · `command/request_payment` | — |
| HTTP gọi | `GET /capture` (điện thoại) | — |
| DB owns | `parking_sessions` · `invoices` | `parking_slots` · `pricing_rules` · `users` |
| Logic | Nhận diện AI · tính tiền · thanh toán | Auth · thống kê · cấu hình |

> 2 BE không gọi nhau. 1 cái crash, cái kia vẫn sống.

---

## Luồng Xe Vào

```
1. ESP32 IR cổng vào phát hiện xe
2. ESP32 MQTT publish → sensors/gate/entry { v:1 }
3. BE1 nhận → HTTP GET /capture → Điện thoại chụp ảnh → trả binary về BE1
4. BE1 chạy AI → ra biển số
5. [async] BE1 upload ảnh → Supabase Storage → lấy image_entry_url
           nếu fail → image_entry_url = null, vẫn tiếp tục
6. BE1 INSERT parking_sessions {
     plate, entry_time,
     status: "active",
     image_entry_url
   }
7. BE1 MQTT publish → command/gate/entry { action: "open", duration: 5 }
8. ESP32 nhận → mở barrier + loa/màn hình thông báo → tự đóng sau 5s
```

---

## Luồng Xe Ra

```
1. ESP32 IR cổng ra phát hiện xe
2. ESP32 MQTT publish → sensors/gate/exit { v:1 }
3. BE1 nhận → HTTP GET /capture → Điện thoại chụp ảnh → trả binary về BE1
4. BE1 chạy AI → ra biển số
5. BE1 query parking_sessions WHERE plate = X AND status = "active"
6. [async] BE1 upload ảnh → Supabase Storage → lấy image_exit_url
           nếu fail → image_exit_url = null, vẫn tiếp tục
7. BE1 tính tiền theo pricing_rules
8. BE1 UPDATE parking_sessions SET {
     exit_time,
     status: "pending_payment",
     image_exit_url
   }
9. BE1 INSERT invoices {
     session_id,
     pricing_rule_id,
     amount,
     duration_minutes,
     status: "pending",
     created_at
   } → nhận lại invoice_id
10. BE1 MQTT publish → command/request_payment {
      session_id,
      invoice_id,
      fee: amount
    }
11. ESP32 nhận → hiển thị màn hình + loa số tiền cần trả
12. ESP32 đếm ngược 3s (fake payment)
13. ESP32 MQTT publish → parking/payment_status {
      invoice_id,
      session_id,
      status: "paid"
    }
14. BE1 nhận →
      UPDATE invoices SET { status: "paid", paid_at: now() } WHERE id = invoice_id
      UPDATE parking_sessions SET { status: "completed" } WHERE id = session_id
15. BE1 MQTT publish → command/gate/exit { action: "open", duration: 5 }
16. ESP32 nhận → mở barrier cổng ra → tự đóng sau 5s
```

---

## Luồng Cảm Biến Slot

```
1. ESP32 IR slot thay đổi
2. MQTT publish → sensors/slot/slot_001 { v:1 }
3. BE2 nhận → UPDATE parking_slots SET status = "occupied"
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
| BE1 timeout 5s | Không mở + báo nhân viên |
| 1 điện thoại 2 sự kiện cùng lúc | BE1 xử lý queue tuần tự |

**Đóng barrier:** ESP32 tự đóng sau `duration` giây do BE1 quyết định — không cần publish `close`. Đảm bảo cổng luôn đóng dù mạng lỗi.

**Cổng ra:** ESP32 đợi BE1 publish `command/gate/exit` mới mở — đảm bảo invoice được ghi nhận trước khi xe ra.

---

## Edge Cases (TODO)

> Phần này sẽ được phát triển sau khi hoàn thành 2 luồng chính.

- [ ] **Upload ảnh fail** — cho phép `image_entry_url` / `image_exit_url = null`, vẫn tiếp tục luồng
- [ ] **Payment timeout** — sau 30s không nhận `parking/payment_status` → auto cancel invoice, ghi log, báo nhân viên

---

<p align="center">
  <a href="../PROBLEM_DEFINITION.md">← Định nghĩa bài toán</a> •
  <a href="../MVP_SCOPE.md">Phạm vi MVP →</a>
</p>