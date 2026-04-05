# System Design — Smart Parking

## Thiết Bị

| Thiết bị | Số lượng | Vai trò |
|----------|----------|---------|
| ESP32 (CP2102) | 1 | 2 IR cổng + 4 IR slot + 2 servo barrier |
| Điện thoại | 1 | Server expose API `/capture` → chụp ảnh trả binary |

---

## Kiến Trúc Tổng Thể

```
                    ┌─────────────────────────┐
                    │        BE Core          │
ESP32 ──MQTT──►  Broker ──►  │                 │──► Supabase
                    │        │  POST /recognize│
ESP32 ◄──MQTT──  Broker ◄──  │                 │
                    └────────┬────────────────┘
                             │         │
                     POST    │         │ SSE push
                  /recognize │         ▼
                    ┌────────▼──┐   Dashboard
                    │  BE LPR   │   (load 1 lần + giữ SSE)
                    └────────┬──┘
                             │ GET /capture
                          Điện thoại
```
> SSE chỉ là phần mở rộng, không cần thiết ở hiện tại 
---

## Phân Chia Trách Nhiệm

| | BE LPR | BE Core |
|--|--------|---------|
| Nhiệm vụ | Capture + AI + Upload | Toàn bộ business logic |
| Gọi | `GET /capture` → Điện thoại | `POST /recognize` → BE LPR |
| Trả về | `{ plate, image_url }` | — |
| MQTT | Không | Subscribe + Publish tất cả |
| SSE | Không | Push event → Dashboard |
| DB | Không đụng | Toàn bộ |
| Stateless | ✅ | ❌ |

> BE LPR không biết DB. BE Core không biết camera. Gọi 1 chiều: Core → LPR.

---

## BE LPR — Xử Lý Ảnh Song Song

```
BE Core gọi POST /recognize { gate: "entry" }
  │
  └─► BE LPR GET /capture → Điện thoại → nhận binary ảnh
        │
        ├─► [Task A] AI nhận diện biển số
        └─► [Task B] Upload ảnh → Supabase Storage
        
        đợi cả 2 xong (asyncio.gather)
        │
        └─► trả { plate: "51A-123", image_url: "https://..." , ... }
```

---

## Luồng Xe Vào

```
1. ESP32 IR cổng vào phát hiện xe
2. ESP32 MQTT publish → sensors/gate/entry { v:1 }
3. BE Core nhận → POST /recognize { gate: "entry" } → BE LPR
4. BE LPR chạy song song AI + upload → trả { plate, image_url }
5. BE Core INSERT parking_sessions {
     plate, entry_time,
     status: "active",
     image_entry_url
   }
6. BE Core MQTT publish → command/gate/entry { action: "open" }
7. ESP32 nhận → mở barrier + loa/màn hình → tự đóng sau 5s
8. `không cần bước này` BE Core SSE push → Dashboard { event: "car_entry", plate, entry_time }  
```

---

## Luồng Xe Ra

```
1. ESP32 IR cổng ra phát hiện xe
2. ESP32 MQTT publish → sensors/gate/exit { v:1 }
3. BE Core nhận → POST /recognize { gate: "exit" } → BE LPR
4. BE LPR chạy song song AI + upload → trả { plate, image_url }
5. BE Core query parking_sessions WHERE plate = X AND status = "active"
6. BE Core tính tiền theo pricing_rules
7. BE Core UPDATE parking_sessions SET {
     exit_time, status: "pending_payment", image_exit_url
   }
8. BE Core INSERT invoices {
     session_id, pricing_rule_id,
     amount, duration_minutes,
     status: "pending", created_at
   } → nhận invoice_id
9. BE Core MQTT publish → command/request_payment {
     session_id, invoice_id, fee: amount
   }
10. ESP32 nhận → hiển thị màn hình + loa số tiền
11. ESP32 đếm ngược 3s (fake payment)
12. ESP32 MQTT publish → parking/payment_status {
      invoice_id, session_id, status: "paid"
    }
13. BE Core nhận →
      UPDATE invoices SET { status: "paid", paid_at: now() } WHERE id = invoice_id
      UPDATE parking_sessions SET { status: "completed" } WHERE id = session_id
14. BE Core MQTT publish → command/gate/exit { action: "open" }
15. ESP32 nhận → mở barrier → tự đóng sau 5s
16. `không cần bước này` BE Core SSE push → Dashboard { event: "car_exit", plate, fee } 
```

---

## Luồng Cảm Biến Slot

```
1. ESP32 IR slot thay đổi
2. ESP32 MQTT publish → sensors/slot/slot_001 { v:1 }
3. BE Core nhận → UPDATE parking_slots SET status = "occupied"
4. BE Core SSE push → Dashboard { event: "slot_updated", slot_id, status }
```

---

## Luồng Heartbeat — Kiểm Soát Phần Cứng

```
1. ESP32 MQTT publish → heartbeat/esp32 { v:1 } mỗi 30s
2. BE Core nhận → cập nhật timestamp last_seen
3. Nếu BE Core không nhận heartbeat > 60s:
     → đánh dấu ESP32 offline
     → SSE push → Dashboard { event: "device_offline", device: "esp32" }  `chưa cần`
     → Cảnh báo nhân viên
```

---

## Barrier Strategy

> Ưu tiên xe không bị kẹt hơn dữ liệu hoàn hảo.

| Tình huống | Xử lý |
|-----------|-------|
| Nhận diện OK, DB OK | Mở barrier |
| Nhận diện OK, DB lỗi | Mở barrier + retry background |
| Không nhận diện được | Mở barrier, plate = `UNKNOWN_{timestamp}` |
| BE LPR timeout | Không mở + SSE push cảnh báo nhân viên |
| 1 điện thoại 2 sự kiện cùng lúc | BE Core xử lý queue tuần tự |

**Đóng barrier:** ESP32 tự đóng sau sau khi xe ra/vào.

**Cổng ra:** ESP32 đợi BE Core publish `command/gate/exit` mới mở — đảm bảo invoice ghi nhận trước khi xe ra.

---

## Edge Cases (TODO)

- [ ] **Upload ảnh fail** — cho phép `image_url = null`, vẫn tiếp tục luồng
- [ ] **Payment timeout** — sau 30s không nhận `payment_status` → auto cancel invoice, ghi log, SSE push cảnh báo
- [ ] **ESP32 offline** — heartbeat timeout → cảnh báo nhân viên qua dashboard

---

<p align="center">
  <a href="../PROBLEM_DEFINITION.md">← Định nghĩa bài toán</a> •
  <a href="../MVP_SCOPE.md">Phạm vi MVP →</a>
</p>
