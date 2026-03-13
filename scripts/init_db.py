import sys
import os

# Đường dẫn gốc của project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from app.utils.supabase import engine
from app.model import Base

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"❌ Lỗi khi khởi tạo database: {e}")

if __name__ == "__main__":
    init_db()

