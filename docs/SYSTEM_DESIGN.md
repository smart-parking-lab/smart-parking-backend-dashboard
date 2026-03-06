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
        API[Routers: auth - slots - bookings<br/>payments - sensors - gates - reports]
    end

    subgraph "Service Layer"
        SVC[Services: Auth - SlotManager - Booking<br/>Pricing - Billing - Payment - Gate - Report]
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
| LPR Service | Backend | **REST POST** | `{ plate_number, image_url, gate_id }` | Gọi khi camera phát hiện xe |
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

### 6.1 Luồng Đăng Ký & Đăng Nhập

```mermaid
sequenceDiagram
    actor U as 👤 User
    participant FE as 📱 Frontend
    participant API as 🌐 FastAPI
    participant AUTH as 🔑 Auth Service
    participant SUPA as ☁️ Supabase Auth
    participant DB as 🗄️ Database

    Note over U,DB: === ĐĂNG KÝ ===
    U->>FE: Nhập email, password, tên
    FE->>API: POST /api/v1/auth/register
    API->>AUTH: register(email, password, name)
    AUTH->>SUPA: supabase.auth.sign_up()
    SUPA-->>AUTH: user_id, access_token
    AUTH->>DB: INSERT profiles (user_id, name, role)
    AUTH-->>API: UserResponse
    API-->>FE: 201 Created + token
    FE-->>U: Đăng ký thành công ✅

    Note over U,DB: === ĐĂNG NHẬP ===
    U->>FE: Nhập email, password
    FE->>API: POST /api/v1/auth/login
    API->>AUTH: login(email, password)
    AUTH->>SUPA: supabase.auth.sign_in_with_password()
    SUPA-->>AUTH: access_token, refresh_token
    AUTH-->>API: TokenResponse
    API-->>FE: 200 OK + tokens
    FE->>FE: Lưu token vào localStorage
    FE-->>U: Đăng nhập thành công ✅
```

### 6.2 Luồng Đặt Chỗ Trước

```mermaid
sequenceDiagram
    actor U as 👤 User
    participant FE as 📱 Frontend
    participant API as 🌐 FastAPI
    participant BOOK as 📋 Booking Service
    participant SLOT as 🅿️ Slot Manager
    participant DB as 🗄️ Database
    participant TIMER as ⏰ Background Task

    U->>FE: Chọn ô đỗ + thời gian
    FE->>API: POST /api/v1/bookings
    API->>BOOK: create_booking(user_id, slot_id, time)
    BOOK->>SLOT: check_slot_available(slot_id)
    SLOT->>DB: SELECT status FROM slots WHERE id = ?
    
    alt Ô đỗ trống
        DB-->>SLOT: status = 'available'
        SLOT-->>BOOK: ✅ Available
        BOOK->>DB: INSERT booking (status='pending')
        BOOK->>DB: UPDATE slot SET status='reserved'
        BOOK->>TIMER: Schedule auto-cancel sau 15 phút
        BOOK-->>API: BookingResponse
        API-->>FE: 201 Created
        FE-->>U: Đặt chỗ thành công ✅

        Note over TIMER,DB: Nếu quá 15 phút mà xe chưa đến
        TIMER->>DB: UPDATE booking SET status='cancelled'
        TIMER->>DB: UPDATE slot SET status='available'
    else Ô đỗ đã có người
        DB-->>SLOT: status = 'occupied'
        SLOT-->>BOOK: ❌ Not available
        BOOK-->>API: raise ConflictException
        API-->>FE: 409 Conflict
        FE-->>U: Ô đỗ đã có người ❌
    end
```

---

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
    subgraph "Client"
        FE[📱 Frontend]
    end

    subgraph "API Gateway"
        CORS[CORS Filter]
        RATE[Rate Limiter]
    end

    subgraph "Authentication"
        JWT_V[JWT Verify]
        SUPA_AUTH[Supabase Auth]
    end

    subgraph "Authorization"
        ROLE[Role Check<br/>User / Admin]
        RLS[Row Level Security<br/>PostgreSQL]
    end

    subgraph "Application"
        API[API Handlers]
        SVC[Services]
    end

    subgraph "Database"
        DB[(PostgreSQL)]
    end

    FE -->|HTTPS + Bearer Token| CORS
    CORS --> RATE
    RATE --> JWT_V
    JWT_V -->|Verify token| SUPA_AUTH
    JWT_V --> ROLE
    ROLE --> API --> SVC --> DB
    DB -.->|RLS Policies| RLS

    style JWT_V fill:#ff5722,color:#fff
    style RLS fill:#ff9800,color:#fff
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
