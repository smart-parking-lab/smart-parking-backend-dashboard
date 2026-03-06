# 📋 Định Nghĩa Bài Toán (Problem Definition)

> Tài liệu phân tích bài toán Hệ thống quản lý bãi đỗ xe thông minh — Smart Parking Management System.

---

## 1. Bối Cảnh

### 🚗 Thực trạng

Tại các bãi đỗ xe ở Việt Nam, phần lớn vẫn vận hành **thủ công**:

| Vấn đề | Mô tả |
|--------|--------|
| **Tìm chỗ đỗ** | Người lái xe phải lái vòng quanh bãi để tìm ô trống, gây mất thời gian và ùn tắc nội bộ |
| **Kiểm soát ra/vào** | Bảo vệ ghi biển số bằng tay, dẫn đến sai sót, tranh cãi và rủi ro mất xe |
| **Tính phí** | Dùng vé giấy, tính phí thủ công, thiếu minh bạch, dễ thất thoát doanh thu |
| **Quản lý vận hành** | Chủ bãi không biết tỷ lệ sử dụng, giờ cao điểm, hay trạng thái cảm biến hỏng |
| **Trải nghiệm người dùng** | Không đặt chỗ trước, không thanh toán online, không biết bãi nào còn chỗ |

### 🎯 Giải pháp đề xuất

Xây dựng hệ thống **tự động hóa toàn bộ quy trình** quản lý bãi đỗ xe:

```
Cảm biến hồng ngoại + ESP32  →  Phát hiện xe tự động
Camera + Nhận diện biển số    →  Kiểm soát ra/vào tự động
Backend + Database            →  Quản lý & tính phí tự động
Mobile/Web App                →  Đặt chỗ & thanh toán online
```

---

## 2. Stakeholders

```mermaid
mindmap
  root((Smart Parking))
    🚗 Người lái xe
      Tìm & đặt chỗ đỗ
      Thanh toán online
      Xem lịch sử
    👨‍💼 Quản lý bãi
      Theo dõi real-time
      Xem báo cáo doanh thu
      Quản lý sự cố
    🏢 Chủ bãi xe
      Báo cáo kinh doanh
      Tối ưu doanh thu
      Mở rộng quy mô
    🔧 Kỹ thuật viên
      Giám sát thiết bị
      Bảo trì cảm biến
      Cập nhật firmware
```

| Stakeholder | Vai trò | Nhu cầu chính |
|-------------|---------|---------------|
| **Người lái xe** | End user | Tìm chỗ nhanh, đặt trước, thanh toán tiện lợi |
| **Quản lý bãi** | Operator | Theo dõi trạng thái real-time, xử lý sự cố |
| **Chủ bãi xe** | Business owner | Tối ưu doanh thu, báo cáo, mở rộng |
| **Kỹ thuật viên** | Maintenance | Giám sát thiết bị, bảo trì phần cứng |

---

## 3. Pain Points & Goals

### ❌ Pain Points (Vấn đề hiện tại)

```mermaid
graph LR
    A[😤 Người lái xe] --> A1[Lái vòng tìm chỗ 10-15 phút]
    A --> A2[Không biết bãi nào còn chỗ]
    A --> A3[Thanh toán tiền mặt bất tiện]
    
    B[😰 Quản lý bãi] --> B1[Ghi biển số tay → sai sót]
    B --> B2[Không biết ô nào trống real-time]
    B --> B3[Tính phí thủ công → thất thoát]
    
    C[📉 Chủ bãi] --> C1[Không có dữ liệu vận hành]
    C --> C2[Không biết giờ cao/thấp điểm]
    C --> C3[Không tối ưu được giá]
```

### ✅ Goals (Mục tiêu)

| # | Goal | Đo lường bằng |
|---|------|---------------|
| G1 | **Tự động phát hiện xe** trong ô đỗ | Độ chính xác cảm biến ≥ 95% |
| G2 | **Tự động kiểm soát ra/vào** bằng biển số | Thời gian xử lý ≤ 5 giây/xe |
| G3 | **Tính phí tự động** dựa trên thời gian đỗ | 0% sai lệch so với thực tế |
| G4 | **Đặt chỗ trước** qua app/web | Tỷ lệ đặt chỗ thành công ≥ 99% |
| G5 | **Dashboard real-time** cho quản lý | Cập nhật trạng thái ≤ 3 giây |
| G6 | **Thanh toán online** (VNPay/Momo) | Hỗ trợ ≥ 2 cổng thanh toán |
| G7 | **Báo cáo doanh thu** tự động | Xuất báo cáo ngày/tháng/năm |

---

## 4. Phạm Vi Hệ Thống

### ✅ Trong phạm vi (In Scope)

```mermaid
graph TB
    subgraph "📡 Thu thập dữ liệu"
        S1[Sensor Listener — MQTT/HTTP]
        S2[Signal Processor — Lọc nhiễu]
        S3[Heartbeat Monitor — Health check]
    end

    subgraph "🚗 Nhận diện & Kiểm soát"
        R1[LPR Engine — Nhận diện biển số]
        R2[Vehicle Matcher — Đối soát]
        R3[Gate Controller — Đóng/mở barie]
        R4[Entry/Exit Logger — Ghi log]
    end

    subgraph "🅿️ Quản lý bãi đỗ"
        P1[Slot Manager — Quản lý ô đỗ]
        P2[Real-time Status — Trạng thái live]
        P3[Pricing Engine — Tính giá]
    end

    subgraph "👤 Người dùng & Đặt chỗ"
        U1[Auth — Đăng ký/Đăng nhập]
        U2[Profile — Quản lý thông tin]
        U3[Booking — Đặt chỗ trước]
    end

    subgraph "💳 Thanh toán"
        PM1[Billing — Hóa đơn]
        PM2[Payment Integration — VNPay/Momo]
        PM3[Transaction Log — Lịch sử]
    end

    subgraph "📊 Giao diện & Báo cáo"
        D1[User Dashboard]
        D2[Admin Dashboard]
        D3[Report Generator]
        D4[Alert System]
    end

    S1 --> S2 --> P2
    R1 --> R2 --> R3
    R3 --> R4
    U3 --> P1
    R4 --> PM1 --> PM2 --> PM3
```

### ❌ Ngoài phạm vi (Out of Scope)

| Tính năng | Lý do loại |
|-----------|-----------|
| Hệ thống EV charging (sạc xe điện) | Phức tạp phần cứng, ngoài scope môn học |
| Đỗ xe tự động (autonomous parking) | Cần xe tự lái |
| Multi-tenant (nhiều bãi xe khác nhau) | MVP chỉ 1 bãi |
| Mobile app native (iOS/Android) | Dùng web responsive thay thế |
| AI dự đoán chỗ đỗ | Nice-to-have, không cần cho MVP |

---

## 5. Yêu Cầu Chức Năng (Functional Requirements)

### Module 1 — Data Acquisition 📡

| ID | Yêu cầu | Priority |
|----|---------|----------|
| FR-1.1 | Hệ thống nhận dữ liệu từ cảm biến hồng ngoại qua MQTT | 🔴 Must |
| FR-1.2 | Lọc nhiễu tín hiệu để xác định trạng thái Trống/Có xe | 🔴 Must |
| FR-1.3 | Phát hiện cảm biến mất kết nối trong vòng 60 giây | 🟡 Should |
| FR-1.4 | Ghi log toàn bộ dữ liệu cảm biến để debug | 🟢 Could |

### Module 3 — Parking Core 🅿️

| ID | Yêu cầu | Priority |
|----|---------|----------|
| FR-3.1 | Quản lý danh sách ô đỗ (thêm, sửa, xóa, phân loại) | 🔴 Must |
| FR-3.2 | Cập nhật trạng thái ô đỗ real-time khi cảm biến thay đổi | 🔴 Must |
| FR-3.3 | Hỗ trợ phân loại ô đỗ: xe máy, ô tô, xe điện | 🟡 Should |
| FR-3.4 | Tính giá dựa trên: loại xe × khung giờ × thời gian đỗ | 🔴 Must |
| FR-3.5 | Hỗ trợ giá theo giờ, theo lượt, theo ngày | 🟡 Should |

### Module 4 — User & Reservation 👤

| ID | Yêu cầu | Priority |
|----|---------|----------|
| FR-4.1 | Đăng ký tài khoản bằng email | 🔴 Must |
| FR-4.2 | Đăng nhập / Đăng xuất an toàn (JWT) | 🔴 Must |
| FR-4.3 | Phân quyền User / Admin | 🔴 Must |
| FR-4.4 | User quản lý danh sách biển số xe | 🟡 Should |
| FR-4.5 | Đặt chỗ trước, giữ chỗ trong 15 phút | 🟡 Should |
| FR-4.6 | Tự động hủy đặt chỗ nếu quá hạn | 🟡 Should |

### Module 5 — Payment 💳

| ID | Yêu cầu | Priority |
|----|---------|----------|
| FR-5.1 | Tạo hóa đơn tự động khi xe rời bãi | 🔴 Must |
| FR-5.2 | Hỗ trợ thanh toán qua VNPay hoặc Momo | 🟡 Should |
| FR-5.3 | Quản lý ví nội bộ (nạp tiền, trừ tiền) | 🟢 Could |
| FR-5.4 | Lưu lịch sử giao dịch đầy đủ | 🔴 Must |

### Module 6 — UI & Analytics 📊

| ID | Yêu cầu | Priority |
|----|---------|----------|
| FR-6.1 | Dashboard user: xem ô trống, đặt chỗ, xem ví | 🔴 Must |
| FR-6.2 | Dashboard admin: bản đồ bãi xe real-time | 🔴 Must |
| FR-6.3 | Báo cáo doanh thu theo ngày/tháng/năm | 🟡 Should |
| FR-6.4 | Cảnh báo khi bãi đầy hoặc cảm biến lỗi | 🟡 Should |

### Module 7 — Utilities 🔧

| ID | Yêu cầu | Priority |
|----|---------|----------|
| FR-7.1 | Hiển thị trạng thái ô đỗ trên màn OLED | 🟡 Should |
| FR-7.2 | Thông báo bằng loa khi xe vào/ra | 🟢 Could |
| FR-7.3 | Sơ đồ bãi xe trực quan trên web | 🔴 Must |

---

## 6. Yêu Cầu Phi Chức Năng (Non-Functional Requirements)

| Loại | Yêu cầu | Chỉ số |
|------|---------|--------|
| ⚡ **Performance** | API response time | ≤ 500ms (P95) |
| ⚡ **Performance** | Cập nhật trạng thái cảm biến | ≤ 3 giây end-to-end |
| ⚡ **Performance** | Concurrent users | ≥ 50 users đồng thời |
| 🔒 **Security** | Authentication | JWT + Supabase Auth |
| 🔒 **Security** | Authorization | Row Level Security (RLS) |
| 🔒 **Security** | Dữ liệu nhạy cảm | Không lưu plain-text password |
| 📈 **Scalability** | Số ô đỗ | ≥ 100 ô đỗ |
| 📈 **Scalability** | Số cảm biến | ≥ 100 cảm biến đồng thời |
| 🔄 **Reliability** | Uptime | ≥ 99% trong giờ hoạt động |
| 🔄 **Reliability** | Mất kết nối cảm biến | Tự động phát hiện trong 60s |
| 🧪 **Testability** | Unit test coverage | ≥ 60% cho services |
| 📱 **Usability** | Responsive | Hoạt động trên mobile browser |

---

## 7. Constraints (Ràng buộc)

| Ràng buộc | Chi tiết |
|-----------|---------|
| **Team size** | 5 thành viên |
| **Thời gian** | Trong khuôn khổ 1 học kỳ (≈ 15 tuần) |
| **Ngân sách** | Miễn phí (Supabase Free tier, MQTT broker miễn phí) |
| **Phần cứng** | ESP32 DevKit + cảm biến hồng ngoại (có sẵn) |
| **Môn học** | Hệ thống Nhúng — cần phần cứng tương tác phần mềm |
| **Demo** | Cần mô hình bãi xe thu nhỏ hoạt động được |

---

## 8. Sơ Đồ Use Case Tổng Quan

```mermaid
graph LR
    subgraph Actors
        U[👤 Người lái xe]
        A[👨‍💼 Admin]
        ESP[📡 ESP32]
        CAM[📷 Camera]
    end

    subgraph "Use Cases"
        UC1[Đăng ký / Đăng nhập]
        UC2[Tìm ô đỗ trống]
        UC3[Đặt chỗ trước]
        UC4[Thanh toán]
        UC5[Xem lịch sử]
        UC6[Theo dõi bãi xe real-time]
        UC7[Quản lý ô đỗ]
        UC8[Xem báo cáo doanh thu]
        UC9[Gửi dữ liệu cảm biến]
        UC10[Nhận diện biển số]
        UC11[Xem hóa đơn]
    end

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC5
    U --> UC11
    A --> UC6
    A --> UC7
    A --> UC8
    ESP --> UC9
    CAM --> UC10
```

---

## 9. Luồng Nghiệp Vụ Chính

### 🚗 Luồng 1: Xe vào bãi

```mermaid
sequenceDiagram
    actor Driver as 🚗 Người lái xe
    participant CAM as 📷 Camera
    participant LPR as 🧠 LPR Engine
    participant BE as 🖥️ Backend
    participant DB as 🗄️ Database
    participant Gate as 🚧 Barie

    Driver->>CAM: Đến cổng vào
    CAM->>LPR: Chụp ảnh biển số
    LPR->>BE: Gửi biển số nhận diện
    BE->>DB: Kiểm tra đặt chỗ / đăng ký
    
    alt Xe hợp lệ
        DB-->>BE: ✅ Có đặt chỗ
        BE->>Gate: Mở barie
        Gate-->>Driver: Barie mở
        BE->>DB: Ghi log xe vào + timestamp
    else Xe không hợp lệ
        DB-->>BE: ❌ Không tìm thấy
        BE->>Gate: Giữ barie đóng
        Gate-->>Driver: Barie đóng + thông báo
    end
```

### 🅿️ Luồng 2: Cảm biến phát hiện xe

```mermaid
sequenceDiagram
    participant IR as 🔴 Cảm biến hồng ngoại
    participant ESP as 📡 ESP32
    participant MQTT as 📨 MQTT Broker
    participant BE as 🖥️ Backend
    participant DB as 🗄️ Database
    participant UI as 📱 Dashboard

    IR->>ESP: Tín hiệu analog/digital
    ESP->>ESP: Đọc & đóng gói JSON
    ESP->>MQTT: Publish topic parking/sensors/slot_01
    MQTT->>BE: Subscribe → nhận message
    BE->>BE: Lọc nhiễu (Signal Processor)
    BE->>DB: UPDATE slot SET status='occupied'
    DB-->>UI: Real-time subscription
    UI-->>UI: Cập nhật sơ đồ bãi xe
```

### 💳 Luồng 3: Xe ra bãi & thanh toán

```mermaid
sequenceDiagram
    actor Driver as 🚗 Người lái xe
    participant CAM as 📷 Camera
    participant LPR as 🧠 LPR Engine
    participant BE as 🖥️ Backend
    participant DB as 🗄️ Database
    participant PAY as 💳 VNPay/Momo
    participant Gate as 🚧 Barie

    Driver->>CAM: Đến cổng ra
    CAM->>LPR: Chụp ảnh biển số
    LPR->>BE: Gửi biển số
    BE->>DB: Query giờ vào
    DB-->>BE: entry_time = 08:30
    BE->>BE: Tính phí (PricingEngine)
    BE->>DB: Tạo hóa đơn (Billing)
    
    alt Thanh toán online
        BE->>PAY: Tạo payment request
        PAY-->>Driver: QR code / Deep link
        Driver->>PAY: Xác nhận thanh toán
        PAY-->>BE: Callback → success
    else Thanh toán ví nội bộ
        BE->>DB: Trừ số dư ví
    end
    
    BE->>Gate: Mở barie
    Gate-->>Driver: Barie mở
    BE->>DB: Ghi log xe ra + transaction
```

---

<p align="center">
  <b>Tài liệu tiếp theo:</b> <a href="SYSTEM_DESIGN.md">🏗️ System Design →</a>
</p>
