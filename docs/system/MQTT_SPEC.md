# MQTT Spec — Smart Parking

---

## MQTT Broker là gì?

MQTT là giao thức nhắn tin nhẹ, thiết kế cho IoT. Hoạt động theo mô hình **Publish / Subscribe** — các thiết bị không giao tiếp trực tiếp với nhau mà thông qua **Broker** làm trung gian.

```
ESP32 ──publish──► Broker ──forward──► BE1
BE1   ──publish──► Broker ──forward──► ESP32
```

- **Publisher** — gửi message lên 1 topic, không cần biết ai đang nhận
- **Subscriber** — đăng ký topic, nhận message khi có ai publish
- **Broker** — trung gian nhận và phân phối message đến đúng subscriber

> Dự án dùng **HiveMQ Cloud** — free tier, managed, không cần tự host.

---


## ESP32 

### Publish

| Topic | Payload | Trigger |
|-------|---------|---------|
| `parking/sensors/gate/entry` | `{"v":1}` · `{"v":0}` | IR cổng vào thay đổi |
| `parking/sensors/gate/exit` | `{"v":1}` · `{"v":0}` | IR cổng ra thay đổi |
| `parking/sensors/slot/slot_001` | `{"v":1}` · `{"v":0}` | IR slot 1 thay đổi |
| `parking/sensors/slot/slot_002` | `{"v":1}` · `{"v":0}` | IR slot 2 thay đổi |
| `parking/heartbeat/esp32` | `{"v":1}` | Mỗi 30s |

### Subscribe

| Topic | Payload | Hành động |
|-------|---------|-----------|
| `parking/command/gate/entry` | `{"action":"open"}` · `{"action":"close"}` | Điều khiển servo cổng vào |
| `parking/command/gate/exit` | `{"action":"open"}` · `{"action":"close"}` | Điều khiển servo cổng ra |

---

## Backend

| | Subscribe | Publish |
|--|-----------|---------|
| BE1 LPR | `parking/sensors/gate/+` | `parking/command/gate/+` |
| BE2 Main | `parking/sensors/slot/#` · `parking/heartbeat/#` | — |

---

## QoS & Retain

| Topic | QoS | Retain |
|-------|-----|--------|
| `sensors/slot/*` | 1 | true |
| `sensors/gate/*` | 1 | false |
| `command/gate/*` | 1 | false |
| `heartbeat/*` | 0 | false |