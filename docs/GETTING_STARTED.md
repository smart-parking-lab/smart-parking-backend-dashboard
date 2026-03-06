# 🚀 Hướng Dẫn Khởi Động Dự Án

> Setup từ A→Z cho thành viên mới tham gia dự án.

---

## 📋 Yêu Cầu Hệ Thống

| Tool | Version | Link cài đặt |
|------|---------|-------------|
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **UV** | latest | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| **Git** | latest | [git-scm.com](https://git-scm.com/) |
| **VS Code** | latest | [code.visualstudio.com](https://code.visualstudio.com/) *(khuyên dùng)* |

---

## 1️⃣ Cài Đặt UV

UV là package manager cực nhanh cho Python (từ Astral — cùng team với Ruff).

<details>
<summary>🪟 Windows (PowerShell)</summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Sau khi cài, kiểm tra:
```powershell
uv --version
```

</details>

<details>
<summary>🐧 Linux / macOS</summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sau khi cài, kiểm tra:
```bash
uv --version
```

</details>

---

## 2️⃣ Clone & Setup Dự Án

```bash
# Clone repo
git clone <repo-url>
cd parking-management-system

# Cài đặt tất cả dependencies (UV tự tạo .venv)
uv sync
```

> [!NOTE]
> UV sẽ tự động tạo thư mục `.venv/` và cài tất cả packages trong `pyproject.toml`.
> Không cần chạy `python -m venv` hay `pip install` thủ công.

---

## 3️⃣ Cấu Hình Biến Môi Trường

```bash
# Copy file mẫu
cp .env.example .env
```

Mở file `.env` và điền thông tin:

```env
# === Supabase ===
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOi...
SUPABASE_SERVICE_KEY=eyJhbGciOi...

# === Database (PostgreSQL qua Supabase) ===
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres

# === MQTT Broker ===
MQTT_BROKER_HOST=broker.hivemq.com
MQTT_BROKER_PORT=1883
MQTT_TOPIC_PREFIX=parking/sensors

# === App ===
APP_ENV=development
APP_DEBUG=true
SECRET_KEY=your-secret-key-here
```

> [!CAUTION]
> **KHÔNG BAO GIỜ** commit file `.env` lên Git. File này đã có trong `.gitignore`.
> Hỏi **Chính**, **Chiến** để lấy thông tin Supabase & MQTT.

---

## 4️⃣ Chạy Dev Server

```bash
# Chạy FastAPI dev server (auto-reload)
uv run fastapi dev src/app/main.py
```

Server sẽ chạy tại: **http://127.0.0.1:8000**

| URL | Mô tả |
|-----|--------|
| `http://127.0.0.1:8000` | API root |
| `http://127.0.0.1:8000/docs` | 📖 Swagger UI (test API) |
| `http://127.0.0.1:8000/redoc` | 📄 ReDoc (API docs đẹp hơn) |

---

## 5️⃣ Các Lệnh Hữu Ích

### Quản Lý Dependencies

```bash
# Thêm package mới
uv add <package-name>

# Thêm dev dependency (chỉ dùng khi phát triển)
uv add --dev <package-name>

# Xóa package
uv remove <package-name>

# Cập nhật tất cả packages
uv sync --upgrade
```

### Kiểm Tra Code

```bash
# Type check với ty
uv run ty check

# Lint với ruff
uv run ruff check .

# Auto-fix lint errors
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Chạy Tests

```bash
# Chạy tất cả tests
uv run pytest

# Chạy test cụ thể
uv run pytest tests/test_auth.py

# Chạy test với output chi tiết
uv run pytest -v
```

---

## 6️⃣ Extensions VS Code Khuyên Dùng

| Extension | Mục đích |
|-----------|----------|
| **Python** (Microsoft) | Hỗ trợ Python cơ bản |
| **ty** (Astral) | Type checking real-time |
| **Ruff** (Astral) | Lint + format tự động |
| **Even Better TOML** | Highlight `pyproject.toml` |
| **Thunder Client** | Test API ngay trong VS Code |

> [!TIP]
> Sau khi cài extensions, mở VS Code Settings (`Ctrl+,`) → tìm `Python: Default Interpreter Path` → đặt thành `.venv/Scripts/python` (Windows) hoặc `.venv/bin/python` (Linux/macOS).

---

## 🔥 Troubleshooting

<details>
<summary>❌ <code>uv: command not found</code></summary>

UV chưa được thêm vào PATH. Thử:
- **Windows**: Mở terminal mới (đóng và mở lại PowerShell)
- **Linux/macOS**: Chạy `source $HOME/.local/bin/env`

Nếu vẫn lỗi, cài lại UV theo hướng dẫn ở [Bước 1](#1️⃣-cài-đặt-uv).

</details>

<details>
<summary>❌ <code>ModuleNotFoundError: No module named 'app'</code></summary>

Đảm bảo chạy từ **thư mục root** của project:
```bash
cd parking-management-system
uv run fastapi dev src/app/main.py
```

Nếu vẫn lỗi, kiểm tra `pyproject.toml` có config đúng:
```toml
[tool.uv]
package = true

[project]
name = "parking-management-system"

[tool.setuptools.packages.find]
where = ["src"]
```

</details>

<details>
<summary>❌ <code>Connection refused</code> khi kết nối Supabase</summary>

1. Kiểm tra file `.env` đã có `SUPABASE_URL` và `SUPABASE_KEY`
2. Kiểm tra URL bắt đầu bằng `https://`
3. Thử mở URL trong trình duyệt xem có truy cập được không
4. Hỏi **Chính** để xác nhận thông tin Supabase

</details>

<details>
<summary>❌ <code>uv sync</code> bị lỗi trên Windows</summary>

Thử chạy PowerShell với quyền **Administrator**:
```powershell
# Mở PowerShell as Administrator
uv sync
```

Hoặc xóa cache và cài lại:
```powershell
uv cache clean
uv sync
```

</details>

---

## ✅ Checklist Sau Setup

Sau khi hoàn thành các bước trên, kiểm tra:

- [ ] `uv --version` hiện version ≥ 0.5
- [ ] `uv run python --version` hiện Python ≥ 3.11
- [ ] `uv run fastapi dev src/app/main.py` chạy không lỗi
- [ ] Mở `http://127.0.0.1:8000/docs` thấy Swagger UI
- [ ] `uv run ty check` chạy không lỗi
- [ ] `uv run ruff check .` chạy không lỗi

---

<p align="center">
  <a href="PROJECT_STRUCTURE.md">← Cấu trúc dự án</a> •
  <a href="GIT_WORKFLOW.md">Quy trình Git →</a>
</p>
