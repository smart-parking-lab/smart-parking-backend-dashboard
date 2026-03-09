<h1 align="center">🅿️ Smart Parking Management System</h1>

<p align="center">
  <b>Hệ thống quản lý bãi đỗ xe thông minh</b><br/>
  Dự án môn học Hệ thống nhúng — Backend chính
</p>

<p align="center">
  <a href="docs/GETTING_STARTED.md">🚀 Bắt đầu</a> •
  <a href="docs/PROJECT_STRUCTURE.md">📁 Cấu trúc dự án</a> •
  <a href="docs/GIT_WORKFLOW.md">🔀 Quy trình Git</a>
</p>

---

## 📋 Giới Thiệu

Hệ thống quản lý bãi đỗ xe thông minh sử dụng **cảm biến hồng ngoại + ESP32** để phát hiện trạng thái ô đỗ theo thời gian thực, kết hợp **nhận diện biển số xe** để tự động kiểm soát ra/vào và tính phí.

> **Repo này** chứa **backend chính** của hệ thống. Module nhận diện biển số xe (LPR) nằm ở [repo riêng](https://github.com/smart-parking-lab/parking-lpr-service).

---



## 📦 Các Module

| # | Nhóm Module | Mô tả | Phụ trách |
|---|------------|--------|-----------|
| 1 | **Data Acquisition** 📡 | Thu thập dữ liệu cảm biến hồng ngoại qua MQTT, lọc nhiễu, kiểm tra heartbeat | Chính |
| 2 | **Recognition & Access** 🚗 | Nhận diện biển số, đối soát, điều khiển barie, ghi log ra/vào | Bằng, Hùng *(repo riêng)* |
| 3 | **Parking Core** 🅿️ | Quản lý ô đỗ, cập nhật trạng thái real-time, tính giá | Tùng |
| 4 | **User & Auth** 👤 | Quản trị Auth, phân quyền, (Dự kiến: profile user) | Hùng, Chiến |
| 5 | **Payment** 💳 | Tạo hóa đơn, tích hợp thanh toán, lưu lịch sử giao dịch | Chiến |
| 6 | **UI & Analytics** 📊 | Dashboard user/admin, báo cáo, hệ thống cảnh báo | Chính |
| 7 | **Utilities** 🔧 | Thông báo (loa + OLED), bản đồ bãi xe | Chính |

> [!NOTE]
> Module 2 (LPR Engine) chạy riêng, giao tiếp với backend qua **REST API**.

---

## 🛠️ Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI |
| **ORM** | SQLAlchemy |
| **Database** | Supabase (PostgreSQL) |
| **Package Manager** | [UV](https://docs.astral.sh/uv/) |
| **Type Checker** | [ty](https://docs.astral.sh/ty/) |
| **Linter** | [Ruff](https://docs.astral.sh/ruff/) |
| **IoT Protocol** | MQTT |
| **Hardware** | ESP32 + Cảm biến hồng ngoại |

---

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/smart-parking-lab/parking-management-system
cd parking-management-system

# Cài đặt dependencies với UV
uv sync

# Copy file env mẫu
cp .env.example .env
# Chỉnh sửa .env với thông tin Supabase & MQTT

# Chạy dev server
uv run fastapi dev src/app/main.py
```

👉 Xem chi tiết tại [**docs/GETTING_STARTED.md**](docs/GETTING_STARTED.md)

---

## 📚 Tài Liệu

| File | Nội dung |
|------|----------|
| [📋 PROBLEM_DEFINITION.md](docs/PROBLEM_DEFINITION.md) | Định nghĩa bài toán, stakeholders, requirements |
| [🏗️ SYSTEM_DESIGN.md](docs/SYSTEM_DESIGN.md) | Thiết kế hệ thống, giao tiếp, MQTT protocol |
| [🎯 MVP_SCOPE.md](docs/MVP_SCOPE.md) | Phạm vi MVP, sprint plan, risk mitigation |
| [🗄️ DATA_MODEL.md](docs/DATA_MODEL.md) | ER diagram, chi tiết bảng, indexes, RLS |
| [🏛️ ARCHITECTURE.md](docs/ARCHITECTURE.md) | Kiến trúc chi tiết, API endpoints, luồng dữ liệu |
| [📁 PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Cấu trúc thư mục, tổ chức code, hướng dẫn thêm mới |
| [🔀 GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) | Luật push code, quy trình PR, commit convention |
| [🚀 GETTING_STARTED.md](docs/GETTING_STARTED.md) | Hướng dẫn cài đặt & khởi động dự án |

---

## 👥 Thành Viên

| Thành viên | Module phụ trách |
|-----------|-----------------|
| **Chính** | Data Acquisition · UI & Analytics · Utilities |
| **Tùng** | Parking Core |
| **Hùng** | Recognition & Access (Lead) · User & Auth |
| **Chiến** | User & Auth · Payment |
| **Bằng** | Recognition & Access |

---

<p align="center">
  <sub>Built with ❤️ for Hệ thống nhúng</sub>
</p>
