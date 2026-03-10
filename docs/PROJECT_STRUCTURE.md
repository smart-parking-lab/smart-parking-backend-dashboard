# 📁 Cấu Trúc Dự Án & Tổ Chức Code

> Tài liệu hướng dẫn cấu trúc thư mục, quy tắc tổ chức code, và cách thêm mới tính năng.

---

## 🗂️ Cây Thư Mục

```
parking-management-system/
│
├── 📄 README.md                     # Tổng quan dự án
├── 📄 pyproject.toml                # Config UV, dependencies, ruff, ty
├── 📄 .env.example                  # Template biến môi trường
├── 📄 .gitignore
│
├── 📂 docs/                         # Tài liệu dự án
│   ├── PROJECT_STRUCTURE.md         # (File này)
│   ├── GIT_WORKFLOW.md              # Quy trình Git
│   └── GETTING_STARTED.md           # Hướng dẫn khởi động
│
├── 📂 src/app/                      # Source code chính
│   ├── main.py                      # 🚪 Entry point FastAPI
│   ├── config.py                    # ⚙️ Settings từ .env
│   ├── dependencies.py              # 💉 Dependency Injection
│   │
│   ├── 📂 core/                     # 🔒 Cross-cutting concerns
│   │   ├── cors.py                  # CORS middleware
│   │   ├── security.py              # JWT & authentication
│   │   ├── exceptions.py            # Custom exception classes
│   │   └── error_handlers.py        # Global error handlers
│   │
│   ├── 📂 models/                   # 🗄️ SQLAlchemy ORM models
│   │   ├── user.py                  # Bảng users
│   │   ├── slot.py                  # Bảng parking_slots
│   │   ├── invoice.py               # Bảng invoices
│   │   └── parking_session.py       # Bảng parking_sessions
│   │
│   ├── 📂 schemas/                  # 📋 Pydantic request/response
│   │   ├── auth.py                  # Login, Register schemas
│   │   ├── slot.py                  # Slot schemas
│   │   ├── payment.py               # Payment schemas
│   │   ├── sensor.py                # Sensor data schemas
│   │   └── gate.py                  # Gate event schemas
│   │
│   ├── 📂 api/v1/                   # 🌐 API Routers
│   │   ├── auth.py                  # /api/v1/auth/*
│   │   ├── slots.py                 # /api/v1/slots/*
│   │   ├── payments.py              # /api/v1/payments/*
│   │   ├── sensors.py               # /api/v1/sensors/*
│   │   ├── gates.py                 # /api/v1/gates/*
│   │   └── reports.py               # /api/v1/reports/*
│   │
│   ├── 📂 services/                 # 🧠 Business logic
│   │   ├── auth_service.py          # Logic đăng ký, đăng nhập
│   │   ├── slot_manager.py          # Quản lý ô đỗ
│   │   ├── pricing_engine.py        # Tính giá
│   │   ├── billing_service.py       # Tạo hóa đơn
│   │   ├── payment_service.py       # Thanh toán VNPay/Momo
│   │   ├── sensor_service.py        # Xử lý data cảm biến
│   │   ├── gate_service.py          # Điều khiển barie
│   │   ├── notification_service.py  # Gửi thông báo
│   │   └── report_service.py        # Tạo báo cáo
│   │
│   ├── 📂 data_acquisition/         # 📡 Module thu thập dữ liệu
│   │   ├── sensor_listener.py       # Lắng nghe MQTT/HTTP
│   │   ├── signal_processor.py      # Lọc nhiễu → trạng thái
│   │   └── heartbeat_monitor.py     # Health check cảm biến
│   │
│   └── 📂 utils/                    # 🧰 Tiện ích dùng chung
│       ├── database.py              # SQLAlchemy engine & session
│       ├── supabase_client.py       # Supabase client init
│       └── mqtt_client.py           # MQTT client wrapper
│
├── 📂 edge/esp32/                   # 🔌 Firmware ESP32
│   └── sensor_firmware/
│       ├── src/main.cpp             # Code đọc cảm biến hồng ngoại
│       └── platformio.ini           # Config PlatformIO
│
└── 📂 tests/                        # 🧪 Unit tests
    ├── conftest.py                  # Fixtures chung
    ├── test_auth.py
    ├── test_slots.py
    └── test_payments.py
```

---

## 🔄 Luồng Xử Lý Request

```
Client Request
     │
     ▼
┌─────────────────┐
│  api/v1/*.py     │  ← Nhận request, validate input
│  (Router)        │
└────────┬────────┘
         │ gọi
         ▼
┌─────────────────┐
│  schemas/*.py    │  ← Validate data với Pydantic
│  (Validation)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  services/*.py   │  ← Xử lý business logic
│  (Logic)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  models/*.py     │  ← Đọc/ghi database qua SQLAlchemy
│  (Database)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Supabase        │  ← PostgreSQL
│  (Storage)       │
└─────────────────┘
```

---

## ⚠️ Phân Biệt `models/` vs `schemas/`

| | `models/` | `schemas/` |
|---|-----------|-----------|
| **Thư viện** | SQLAlchemy | Pydantic |
| **Mục đích** | Ánh xạ bảng DB (ORM) | Validate request/response |
| **Ví dụ** | `class User(Base)` | `class UserCreate(BaseModel)` |
| **Dùng ở** | `services/` | `api/` |

<details>
<summary>📌 Ví dụ minh họa</summary>

**`models/user.py`** — SQLAlchemy model:
```python
from sqlalchemy import Column, String, Boolean
from app.utils.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    is_admin = Column(Boolean, default=False)
```

**`schemas/auth.py`** — Pydantic schema:
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_admin: bool

    class Config:
        from_attributes = True  # Cho phép convert từ SQLAlchemy model
```

</details>

---

## 🔒 Thư Mục `core/` — Cross-cutting Concerns

| File | Vai trò |
|------|---------|
| `cors.py` | Cấu hình CORS origins, methods, headers |
| `security.py` | Verify JWT token, get current user, phân quyền |
| `exceptions.py` | Định nghĩa custom exceptions (`NotFoundException`, `ForbiddenException`...) |
| `error_handlers.py` | Đăng ký global exception handlers cho FastAPI app |

<details>
<summary>📌 Ví dụ error handling tập trung</summary>

**`core/exceptions.py`**:
```python
class AppException(Exception):
    """Base exception cho toàn bộ app."""
    def __init__(self, status_code: int, detail: str, error_code: str | None = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

class NotFoundException(AppException):
    def __init__(self, detail: str = "Không tìm thấy"):
        super().__init__(status_code=404, detail=detail, error_code="NOT_FOUND")

class ForbiddenException(AppException):
    def __init__(self, detail: str = "Không có quyền truy cập"):
        super().__init__(status_code=403, detail=detail, error_code="FORBIDDEN")
```

**`core/error_handlers.py`**:
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
            }
        }
    )

def register_error_handlers(app):
    """Gọi trong main.py để đăng ký tất cả handlers."""
    app.add_exception_handler(AppException, app_exception_handler)
```

**Sử dụng trong service**:
```python
from app.core.exceptions import NotFoundException

class SlotManager:
    def get_slot(self, slot_id: str):
        slot = db.query(Slot).get(slot_id)
        if not slot:
            raise NotFoundException(f"Ô đỗ {slot_id} không tồn tại")
        return slot
```

</details>

---

## 📝 Quy Ước Đặt Tên

| Đối tượng | Quy tắc | Ví dụ |
|----------|---------|-------|
| **File** | `snake_case.py` | `slot_manager.py` |
| **Class** | `PascalCase` | `SlotManager` |
| **Function** | `snake_case` | `get_available_slots()` |
| **Variable** | `snake_case` | `slot_count` |
| **Constant** | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| **API route** | `kebab-case` | `/api/v1/parking-slots` |
| **DB table** | `snake_case` (số nhiều) | `parking_slots` |

---

## ➕ Hướng Dẫn Thêm Mới

### 1. Thêm API Endpoint Mới

> Ví dụ: Thêm endpoint `GET /api/v1/slots/{id}/history`

```
Bước 1 → schemas/slot.py          Thêm SlotHistoryResponse
Bước 2 → services/slot_manager.py Thêm method get_slot_history()
Bước 3 → api/v1/slots.py          Thêm route @router.get("/{id}/history")
Bước 4 → tests/test_slots.py      Thêm test case
```

<details>
<summary>📌 Code mẫu chi tiết</summary>

**Bước 1 — `schemas/slot.py`**:
```python
class SlotHistoryResponse(BaseModel):
    slot_id: str
    status: str
    changed_at: datetime
    
    class Config:
        from_attributes = True
```

**Bước 2 — `services/slot_manager.py`**:
```python
class SlotManager:
    def get_slot_history(self, db: Session, slot_id: str) -> list[SlotHistory]:
        slot = db.query(Slot).get(slot_id)
        if not slot:
            raise NotFoundException(f"Ô đỗ {slot_id} không tồn tại")
        return db.query(SlotHistory).filter_by(slot_id=slot_id).all()
```

**Bước 3 — `api/v1/slots.py`**:
```python
@router.get("/{slot_id}/history", response_model=list[SlotHistoryResponse])
async def get_slot_history(
    slot_id: str,
    db: Session = Depends(get_db),
    slot_manager: SlotManager = Depends()
):
    return slot_manager.get_slot_history(db, slot_id)
```

</details>

---

### 2. Thêm Bảng Database Mới

> Ví dụ: Thêm bảng `notifications`

```
Bước 1 → models/notification.py   Tạo SQLAlchemy model
Bước 2 → schemas/notification.py   Tạo Pydantic schemas
Bước 3 → models/__init__.py        Export model mới
Bước 4 → Chạy migration (Supabase) Tạo bảng trong DB
```

---

### 3. Thêm Service Mới

> Ví dụ: Thêm `notification_service.py`

```
Bước 1 → services/notification_service.py  Tạo class NotificationService
Bước 2 → dependencies.py                    Đăng ký dependency (nếu cần)
Bước 3 → api/v1/ tương ứng                  Import và sử dụng
```

---

### 4. Thêm Module Hoàn Toàn Mới

> Khi cần thêm một nhóm tính năng lớn (tương tự `data_acquisition/`)

```
Bước 1 → Tạo thư mục src/app/<tên_module>/
Bước 2 → Tạo __init__.py
Bước 3 → Tạo các file logic bên trong
Bước 4 → Đăng ký vào main.py (nếu cần startup/shutdown)
Bước 5 → Cập nhật docs/PROJECT_STRUCTURE.md
```

---

## 🔗 Quy Tắc Import

```python
# ✅ Import tuyệt đối (luôn dùng cách này)
from app.models.user import User
from app.schemas.auth import UserCreate
from app.services.auth_service import AuthService
from app.core.exceptions import NotFoundException
from app.utils.database import get_db

# ❌ Import tương đối (KHÔNG dùng)
from ..models.user import User
from .exceptions import NotFoundException
```

> [!TIP]
> Luôn dùng **import tuyệt đối** bắt đầu từ `app.` để tránh lỗi khi chạy từ thư mục khác nhau.

---

<p align="center">
  <a href="GIT_WORKFLOW.md">Tiếp: 🔀 Quy trình Git →</a>
</p>
