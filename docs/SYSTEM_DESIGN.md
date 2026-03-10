# 🏗️ System Design — Thiết Kế Hệ Thống

> Tài liệu thiết kế hệ thống tổng thể cho Smart Parking Management System.

---

## 1. System Context

Hệ thống giao tiếp với các thành phần bên ngoài:

```mermaid
graph TB
    subgraph "External"
        U[👤 Người dùng<br/>Web Browser]
        ESP[📡 ESP32<br/>Cảm biến hồng ngoại]
        LPR[📷 LPR Service<br/>Repo riêng]
        PAY[💳 VNPay / Momo<br/>Payment Gateway]
        MQTT_B[📨 MQTT Broker<br/>HiveMQ / Mosquitto]
    end

    subgraph "Smart Parking Backend"
        API[🌐 FastAPI Server]
    end

    subgraph "Data Layer"
        DB[(🗄️ Supabase<br/>PostgreSQL + Realtime)]
    end

    U -->|REST API| API
    U -.->|Supabase Realtime| DB
    ESP -->|MQTT Publish| MQTT_B
    MQTT_B -->|MQTT Subscribe| API
    LPR -->|REST API| API
    API -->|REST API| PAY
    PAY -->|Callback| API
    API -->|Read/Write| DB

    style API fill:#009688,color:#fff
    style DB fill:#3FCF8E,color:#fff
    style ESP fill:#E7352C,color:#fff
```

---

## 2. High-Level Components

```mermaid
graph TD
    subgraph "API Layer"
        API[Routers: auth - slots - payments<br/>sensors - gates - reports]
    end

    subgraph "Service Layer"
        SVC[Services: Auth - SlotManager - Pricing<br/>Billing - Payment - Gate - Report]
    end

    subgraph "Data Acquisition"
        DAQ[MQTT Listener - Signal Processor - Heartbeat]
    end

    subgraph "Core"
        CORE[CORS - JWT Security - Error Handlers]
    end

    subgraph "Data Layer"
        DATA[SQLAlchemy ORM - Supabase Client - MQTT Client]
        DB[(PostgreSQL)]
    end

    CORE --> API --> SVC --> DATA --> DB
    DAQ --> SVC

    style CORE fill:#ff5722,color:#fff
    style DB fill:#3FCF8E,color:#fff
```

---

## 3. Giao Tiếp Giữa Các Hệ Thống Con

| Từ | Đến | Phương thức | Dữ liệu | Ghi chú |
|----|-----|------------|----------|---------|
| ESP32 | MQTT Broker | **MQTT Publish** | `{ slot_id, value, timestamp }` | Topic: `parking/sensors/{slot_id}` |
| MQTT Broker | Backend | **MQTT Subscribe** | Tương tự trên | Backend subscribe topic wildcard |
| LPR Service | Backend | **REST POST** | `multipart/form-data` (plate_number, gate_id, image_file) | Upload ảnh qua file đính kèm |
| Backend | Supabase Storage | **API Upload** | Image binary | Backend upload ảnh lên bucket, nhận `public_url` gắn vào database |
| Backend | VNPay/Momo | **REST POST** | `{ amount, order_id, return_url }` | Tạo payment request |
| VNPay/Momo | Backend | **HTTP Callback** | `{ status, transaction_id }` | IPN callback khi thanh toán xong |
| Backend | Supabase | **PostgreSQL** | SQL queries | Qua SQLAlchemy ORM |
| Supabase | Frontend | **Supabase Realtime** | `{ slot_id, status, updated_at }` | Frontend subscribe trực tiếp, không qua backend |

---

## 4. Chi Tiết Protocol MQTT

### Topic Structure

```
parking/
├── sensors/
│   ├── slot_001          # Dữ liệu từ cảm biến ô đỗ 001
│   ├── slot_002
│   └── ...
├── heartbeat/
│   ├── esp32_01          # Heartbeat từ ESP32 board 01
│   └── ...
└── commands/
    └── gate/             # Lệnh đóng/mở barie
```

### Payload Format

```json
// Topic: parking/sensors/slot_001
{
  "slot_id": "slot_001",
  "value": 1,
  "raw_value": 2847,
  "board_id": "esp32_01",
  "timestamp": 1709712000
}
```

| Field | Type | Mô tả |
|-------|------|--------|
| `slot_id` | string | ID ô đỗ |
| `value` | int | `1` = có xe, `0` = trống |
| `raw_value` | int | Giá trị thô từ cảm biến (debug) |
| `board_id` | string | ID board ESP32 |
| `timestamp` | int | Unix timestamp |

### QoS & Retention

| Setting | Giá trị | Lý do |
|---------|---------|-------|
| QoS | **1** (At least once) | Đảm bảo data không mất, chấp nhận duplicate |
| Retain | **true** | Khi backend restart, nhận được state cuối cùng |
| Keep Alive | **60s** | Phát hiện mất kết nối nhanh |

---

## 5. Công Nghệ & Lý Do Chọn

| Thành phần | Công nghệ | Lý do |
|-----------|-----------|-------|
| **Backend Framework** | FastAPI | Async, auto docs (Swagger), type hints, performance tốt |
| **ORM** | SQLAlchemy | Mature, relationship mapping mạnh, migration support |
| **Database** | Supabase (PostgreSQL) | Free tier đủ dùng, built-in Auth/RLS, Realtime subscriptions |
| **Package Manager** | UV | Nhanh gấp 10-100x pip, lockfile chính xác, từ Astral |
| **Type Checker** | ty | Nhanh gấp 10-100x mypy, từ Astral, tích hợp tốt với UV |
| **Linter** | Ruff | Nhanh, thay thế cả flake8 + isort + black, từ Astral |
| **IoT Protocol** | MQTT | Lightweight, pub/sub phù hợp IoT, hỗ trợ QoS |
| **MQTT Broker** | HiveMQ Cloud | Free tier, managed, không cần tự host |
| **Auth** | Supabase Auth + JWT | Sẵn có, hỗ trợ OAuth, email/password |
| **Microcontroller** | ESP32 | WiFi built-in, GPIO đủ, Arduino/PlatformIO support |
| **Cảm biến** | Hồng ngoại (IR) | Rẻ, đơn giản, phát hiện vật cản chính xác |

---

## 6. Sequence Diagrams Chi Tiết

*(Các Sequence Diagram chi tiết về luồng xe chạy đã được di chuyển sang file ARCHITECTURE.md mục 2)*

## 7. Error Handling Strategy

### Phân Loại Lỗi

```mermaid
graph TD
    ERR[Lỗi phát sinh] --> CLIENT[Client Error 4xx]
    ERR --> SERVER[Server Error 5xx]
    ERR --> INFRA[Infrastructure Error]

    CLIENT --> C1[400 Bad Request<br/>Dữ liệu không hợp lệ]
    CLIENT --> C2[401 Unauthorized<br/>Chưa đăng nhập]
    CLIENT --> C3[403 Forbidden<br/>Không có quyền]
    CLIENT --> C4[404 Not Found<br/>Không tìm thấy]
    CLIENT --> C5[409 Conflict<br/>Trùng lặp/xung đột]

    SERVER --> S1[500 Internal<br/>Lỗi không mong đợi]

    INFRA --> I1[MQTT Broker mất kết nối]
    INFRA --> I2[Supabase timeout]
    INFRA --> I3[Cảm biến mất tín hiệu]
```

### Response Format Thống Nhất

```json
// ✅ Success
{
  "success": true,
  "data": { ... },
  "message": "Thao tác thành công"
}

// ❌ Error
{
  "success": false,
  "error": {
    "code": "SLOT_NOT_FOUND",
    "message": "Ô đỗ slot_042 không tồn tại",
    "details": null
  }
}
```

### Error Codes

| Code | HTTP | Mô tả |
|------|------|--------|
| `VALIDATION_ERROR` | 400 | Dữ liệu request không hợp lệ |
| `UNAUTHORIZED` | 401 | Token hết hạn hoặc không hợp lệ |
| `FORBIDDEN` | 403 | Không có quyền thực hiện thao tác |
| `NOT_FOUND` | 404 | Resource không tồn tại |
| `SLOT_NOT_AVAILABLE` | 409 | Ô đỗ đã có xe hoặc đã được đặt |
| `BOOKING_EXPIRED` | 409 | Đặt chỗ đã hết hạn |
| `INSUFFICIENT_BALANCE` | 402 | Số dư ví không đủ |
| `PAYMENT_FAILED` | 502 | Cổng thanh toán lỗi |
| `SENSOR_OFFLINE` | 503 | Cảm biến mất kết nối |
| `INTERNAL_ERROR` | 500 | Lỗi server không xác định |

---

## 8. Security Architecture

```mermaid
graph LR
    subgraph "Clients & Services"
        FE[📱 Web Frontend]
        LPR[📷 LPR Service<br/>Backend 2]
    end

    subgraph "API Gateway"
        CORS[CORS Filter]
        RATE[Rate Limiter]
    end

    subgraph "Security Check"
        JWT_V[Xác thực bằng JWT<br/>Frontend]
        API_KEY[Xác thực bằng API KEY<br/>Service to Service]
    end

    subgraph "Application"
        API[API Handlers]
    end

    subgraph "Database"
        DB[(PostgreSQL)]
    end

    FE -->|HTTPs + Bearer JWT| CORS
    LPR -->|HTTPs + Mật khẩu API_KEY| CORS
    CORS --> RATE
    RATE --> JWT_V
    RATE --> API_KEY
    JWT_V --> API
    API_KEY --> API
    API --> DB

    style JWT_V fill:#ff5722,color:#fff
    style API_KEY fill:#ff9800,color:#fff
```

### Các Lớp Bảo Mật

| Lớp | Cơ chế | Mô tả |
|-----|--------|--------|
| **Transport** | HTTPS | Mã hóa toàn bộ traffic |
| **CORS** | Whitelist origins | Chỉ cho phép domain frontend |
| **Rate Limiting** | Token bucket | Chống brute force, DDoS |
| **Authentication** | JWT (Supabase) | Xác thực người dùng |
| **Authorization** | Role-based (User/Admin) | Phân quyền theo vai trò |
| **Data** | RLS (PostgreSQL) | User chỉ thấy data của mình |
| **Input** | Pydantic validation | Validate mọi input từ client |
| **Secrets** | `.env` + Supabase Vault | Không hardcode secrets |

---

## 9. Deployment Overview

```mermaid
graph TB
    subgraph "Development"
        DEV[💻 Local Machine]
        UV_DEV[UV + FastAPI dev]
    end

    subgraph "Cloud Services"
        SUPA_CLOUD[☁️ Supabase Cloud<br/>Database + Auth + Realtime]
        MQTT_CLOUD[📨 HiveMQ Cloud<br/>MQTT Broker]
    end

    subgraph "Edge Devices"
        ESP_1[📡 ESP32 #1<br/>Khu A - 10 ô đỗ]
        ESP_2[📡 ESP32 #2<br/>Khu B - 10 ô đỗ]
        CAM[📷 Camera<br/>Cổng vào/ra]
    end

    DEV -->|SQL + REST| SUPA_CLOUD
    DEV -->|MQTT Subscribe| MQTT_CLOUD
    ESP_1 -->|MQTT Publish| MQTT_CLOUD
    ESP_2 -->|MQTT Publish| MQTT_CLOUD
    CAM -->|REST API| DEV

    style SUPA_CLOUD fill:#3FCF8E,color:#fff
    style MQTT_CLOUD fill:#660066,color:#fff
    style ESP_1 fill:#E7352C,color:#fff
    style ESP_2 fill:#E7352C,color:#fff
```

> [!NOTE]
> **Môi trường demo**: Backend chạy trên máy local, kết nối Supabase Cloud và HiveMQ Cloud. ESP32 kết nối WiFi cùng mạng LAN hoặc qua internet.

---

<p align="center">
  <a href="PROBLEM_DEFINITION.md">← Định nghĩa bài toán</a> •
  <a href="MVP_SCOPE.md">Phạm vi MVP →</a>
</p>
