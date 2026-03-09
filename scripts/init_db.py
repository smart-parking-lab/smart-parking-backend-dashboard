import sys
import os

# Đường dẫn gốc của project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.app.utils.supabase import engine
from src.app.model import Base

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"❌ Lỗi khi khởi tạo database: {e}")

if __name__ == "__main__":
    init_db()

