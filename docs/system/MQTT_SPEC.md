# MQTT Spec — Smart Parking

> Broker: **HiveMQ Cloud** — free tier, managed, không cần tự host.

---

## MQTT là gì?

Giao thức nhắn tin nhẹ cho IoT, hoạt động theo mô hình **Publish / Subscribe** qua Broker làm trung gian.

```
ESP32 ──publish──► Broker ──forward──► BE1
BE1   ──publish──► Broker ──forward──► ESP32
```

- **Publisher** — gửi message lên topic, không cần biết ai nhận
- **Subscriber** — đăng ký topic, tự nhận khi có message
- **Broker** — trung gian phân phối đúng subscriber

---

## ESP32 — Publish

| Topic | Payload | Trigger |
|-------|---------|---------|
| `parking/sensors/gate/entry` | `{"v":1\|0}` | IR cổng vào thay đổi |
| `parking/sensors/gate/exit` | `{"v":1\|0}` | IR cổng ra thay đổi |
| `parking/sensors/slot/slot_001` | `{"v":1\|0}` | IR slot 1 thay đổi |
| `parking/sensors/slot/slot_002` | `{"v":1\|0}` | IR slot 2 thay đổi |
| `parking/sensors/slot/slot_004` | `{"v":1\|0}` | IR slot 4 thay đổi |
| `parking/payment_status` | `{"invoice_id":"...","session_id":"...","status":"paid"}` | Sau đếm ngược xong |
| `parking/heartbeat/esp32` | `{"v":1}` | Mỗi 30s |

---

## ESP32 — Subscribe

| Topic | Payload | Hành động |
|-------|---------|-----------|
| `parking/command/gate/entry` | `{"action":"open","duration":5}` | Servo cổng vào → tự đóng sau `duration`s |
| `parking/command/gate/exit` | `{"action":"open","duration":5}` | Servo cổng ra → tự đóng sau `duration`s |
| `parking/command/request_payment` | `{"invoice_id":"...","session_id":"...","fee":13000}` | Hiển thị màn hình + loa → đếm ngược → publish payment_status |

---

## Backend

| | Subscribe | Publish |
|--|-----------|---------|
| BE1 LPR | `sensors/gate/+` · `payment_status` | `command/gate/+` · `command/request_payment` |
| BE2 Main | `sensors/slot/#` · `heartbeat/#` | — |

---

## QoS & Retain

| Topic | QoS | Retain |
|-------|-----|--------|
| `sensors/slot/*` | 1 | true |
| `sensors/gate/*` | 1 | false |
| `payment_status` | 1 | false |
| `command/gate/*` | 1 | false |
| `command/request_payment` | 1 | false |
| `heartbeat/*` | 0 | false |