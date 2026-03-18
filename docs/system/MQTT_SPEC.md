## Topics

### ESP32 — Cổng vào (tương tự ra)

| Hành động | Topic | Payload |
|-----------|-------|---------|
| **Publish** | `parking/sensors/gate/entry` | `{ "v": 1 }` có xe <br> `{ "v": 0 }` không có |
| **Subscribe** | `parking/command/gate/entry` | `{ "action": "open" }` <br> `{ "action": "close" }` |
| **Publish** | `parking/heartbeat/{gate}` | `{ "v": 1 }` mỗi 30s |


### ESP32 — Slot

| Hành động | Topic | Payload |
|-----------|-------|---------|
| **Publish** | `parking/sensors/slot/{slot_id}` | `{ "v": 1 }` có xe <br> `{ "v": 0 }` trống |
| **Publish** | `parking/heartbeat/{slot_id}` | `{ "v": 1 }` mỗi 30s |

---

## Backend Subscribe/Publish

| Backend | Subscribe | Publish |
|---------|-----------|---------|
| BE1 LPR | `parking/sensors/gate/entry` `parking/sensors/gate/exit` | `parking/command/gate/entry` `parking/command/gate/exit` |
| BE2 Main | `parking/sensors/slot/{slot_id}` `parking/heartbeat/#` | — |

---

## QoS & Retain

| Topic | QoS | Retain |
|-------|-----|--------|
| `sensors/slot/*` | 1 | true |
| `sensors/gate/*` | 1 | false |
| `command/gate/*` | 1 | false |
| `heartbeat/*` | 0 | false |