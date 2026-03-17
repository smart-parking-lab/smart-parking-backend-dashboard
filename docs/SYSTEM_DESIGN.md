# 🏗️ System Design — Thiết Kế Hệ Thống

> Tài liệu thiết kế hệ thống tổng thể cho Smart Parking Management System.

---

## 1. System Context

Hệ thống gồm 2 backend độc lập, giao tiếp với các thành phần bên ngoài:

```mermaid
graph TB
    subgraph "External Devices"
        CAM[📷 ESP32 Camera<br/>Cổng vào / ra]
        SEN[📡 ESP32 Cảm biến<br/>Từng ô đỗ]
    end

    subgraph "Backend 1 — LPR Service (Python/FastAPI)"
        LPR[🤖 Nhận diện biển số<br/>+ Quản lý parking_sessions<br/>+ Tính tiền]
    end

    subgraph "Backend 2 — Main Service (Python/FastAPI)"
        MAIN[🌐 Auth · Dashboard<br/>Pricing Config · Lịch sử<br/>Sửa thủ công]
    end

    subgraph "Data Layer"
        DB[(🗄️ Supabase<br/>PostgreSQL + Realtime + Storage)]
    end

    subgraph "Frontend"
        FE[💻 Web Dashboard<br/>Admin / Nhân viên]
    end

    CAM -->|multipart/form-data ảnh thẳng| LPR
    LPR -->|Trả response barrier open/close| CAM
    LPR -->|INSERT / UPDATE parking_sessions| DB
    LPR -->|async upload ảnh| DB

    SEN -->|REST API trực tiếp| DB

    MAIN -->|CRUD auth, config, lịch sử| DB
    FE -->|REST API + JWT| MAIN
    FE -.->|Supabase Realtime| DB

    style LPR fill:#1565C0,color:#fff
    style MAIN fill:#009688,color:#fff
    style DB fill:#3FCF8E,color:#fff
    style CAM fill:#E7352C,color:#fff
    style SEN fill:#E7352C,color:#fff
```

---

## 2. Phân Chia Trách Nhiệm Rõ Ràng

| | Backend 1 — LPR Service | Backend 2 — Main Service |
|---|---|---|
| **Vai trò** | Xử lý luồng xe vào/ra | Quản lý hệ thống |
| **Owns table** | `parking_sessions` | `users`, `pricing_config`, `parking_slots` (config) |
| **Trigger** | ESP32 Camera gửi ảnh | Web Dashboard, Admin |
| **Logic** | Nhận diện AI + tính tiền | Auth, thống kê, cấu hình |
| **Barrier** | Trả lệnh mở/đóng | Không liên quan |

> **Nguyên tắc:** 2 BE **không gọi nhau**, đều đọc/ghi Supabase trực tiếp. Tách concern rõ ràng, 1 cái crash cái kia vẫn sống.

---

## 3. Luồng Xe Vào Chi Tiết

```mermaid
sequenceDiagram
    participant CAM as 📷 ESP32 Camera
    participant LPR as 🤖 BE1 LPR Service
    participant DB as 🗄️ Supabase
    participant BAR as 🚧 Barrier

    CAM->>LPR: POST /recognize (multipart ảnh)
    LPR->>LPR: Chạy model AI nhận diện biển số
    LPR->>DB: Query pricing_config (lấy giá hiện tại)
    DB-->>LPR: { price_per_hour, ... }
    LPR->>DB: INSERT parking_sessions { plate, entry_time, status: active }
    DB-->>LPR: { session_id, ... }
    LPR-->>CAM: { success: true, plate: "51A-123", session_id }
    CAM->>BAR: Mở barrier (PWM signal)
    Note over LPR,DB: async — không chặn barrier
    LPR->>DB: Upload ảnh → Supabase Storage (lấy public_url)
    LPR->>DB: UPDATE parking_sessions SET image_entry_url
```

---

## 4. Luồng Xe Ra Chi Tiết

```mermaid
sequenceDiagram
    participant CAM as 📷 ESP32 Camera
    participant LPR as 🤖 BE1 LPR Service
    participant DB as 🗄️ Supabase
    participant BAR as 🚧 Barrier
    participant LCD as 🖥️ LCD Display

    CAM->>LPR: POST /recognize (multipart ảnh)
    LPR->>LPR: Chạy model AI nhận diện biển số
    LPR->>DB: Query parking_sessions WHERE plate = X AND status = active
    DB-->>LPR: { session_id, entry_time, slot_id }
    LPR->>DB: Query pricing_config (giá theo giờ hiện tại)
    LPR->>LPR: Tính tiền (xử lý đêm/ngày)
    LPR->>DB: UPDATE parking_sessions { exit_time, duration, fee, status: completed }
    LPR-->>CAM: { success: true, fee: 13000, duration: 90 }
    CAM->>LCD: Hiển thị số tiền
    CAM->>BAR: Mở barrier
    Note over LPR,DB: async
    LPR->>DB: Upload ảnh ra → Storage
    LPR->>DB: UPDATE parking_sessions SET image_exit_url
```

---

## 5. Luồng Cảm Biến Ô Đỗ

```mermaid
sequenceDiagram
    participant SEN as 📡 ESP32 Cảm biến
    participant DB as 🗄️ Supabase
    participant FE as 💻 Dashboard

    SEN->>DB: PATCH /parking_slots?id=eq.{slot_id}<br/>{ status: "occupied" }
    DB-->>SEN: 200 OK
    DB-)FE: Supabase Realtime push { slot_id, status }
    FE->>FE: Cập nhật sơ đồ bãi xe real-time
```

> ESP32 cảm biến gọi **thẳng Supabase REST API** — không cần qua backend nào. Logic đơn giản, giảm tải hoàn toàn cho cả 2 BE.

---

## 6. Công Nghệ Sử Dụng

| Thành phần | Công nghệ | Lý do |
|-----------|-----------|-------|
| **BE1 LPR** | Python FastAPI | Async, tích hợp AI/ML dễ |
| **BE2 Main** | Python FastAPI | Đồng nhất stack, auto Swagger |
| **ORM** | SQLAlchemy | Mature, migration support |
| **Database** | Supabase (PostgreSQL) | Free tier, Realtime, Auth, Storage sẵn |
| **Realtime** | Supabase Realtime | Dashboard cập nhật sơ đồ bãi xe |
| **Storage** | Supabase Storage | Lưu ảnh biển số vào/ra |
| **IoT** | ESP32 WiFi | Built-in WiFi, GPIO đủ dùng |
| **Cảm biến** | Hồng ngoại (IR) | Đơn giản, chính xác, rẻ |
| **Package Manager** | UV | Nhanh hơn pip 10-100x |
| **Linter** | Ruff | Thay thế flake8 + black + isort |
| **Payment** | Tiền mặt (v1) | Đơn giản, đủ cho MVP — nâng cấp VNPay/Momo sau |

---

## 7. Deployment Overview

```mermaid
graph TB
    subgraph "Local Machine (Demo)"
        BE1[🤖 BE1 LPR Service<br/>terminal 1 — port 8001]
        BE2[🌐 BE2 Main Service<br/>terminal 2 — port 8000]
    end

    subgraph "Cloud"
        SUPA[☁️ Supabase Cloud<br/>DB + Auth + Storage + Realtime]
    end

    subgraph "Edge Devices"
        CAM[📷 ESP32 Camera Gate]
        SEN1[📡 ESP32 Cảm biến Khu A]
        SEN2[📡 ESP32 Cảm biến Khu B]
    end

    CAM -->|LAN / WiFi| BE1
    BE1 --> SUPA
    BE2 --> SUPA
    SEN1 -->|WiFi → Internet| SUPA
    SEN2 -->|WiFi → Internet| SUPA

    style SUPA fill:#3FCF8E,color:#fff
    style BE1 fill:#1565C0,color:#fff
    style BE2 fill:#009688,color:#fff
```

> **Môi trường demo:** 2 backend chạy local (2 terminal), kết nối Supabase Cloud. ESP32 cùng mạng LAN hoặc qua internet.

---

## 8. Bottleneck & Optimization

> Optimize đúng chỗ, không waste thời gian vào những thứ không phải vấn đề.

| Yếu tố | Ảnh hưởng | Hành động |
|--------|-----------|-----------|
| ESP32 WiFi upload ảnh | ⚠️ Cao | Resize ảnh về 640×480 trước khi gửi |
| Model AI nhận diện | ⚠️ Cao | Dùng model nhẹ (YOLOv8n + EasyOCR) |
| Upload Storage (ảnh) | ✅ Không chặn | Chạy async sau khi mở barrier |
| HTTP call giữa 2 BE | ✅ Không có | 2 BE không gọi nhau |
| Supabase write | ✅ Chấp nhận được | ~100ms, không ảnh hưởng UX |

**Thứ tự ưu tiên tối ưu:**
1. Chất lượng + kích thước ảnh từ ESP32
2. Tốc độ model AI (inference time)
3. Ổn định WiFi tại cổng vào/ra

---

<p align="center">
  <a href="PROBLEM_DEFINITION.md">← Định nghĩa bài toán</a> •
  <a href="MVP_SCOPE.md">Phạm vi MVP →</a>
</p>
