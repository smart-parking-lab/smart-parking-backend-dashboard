import sys
import os
import hashlib

# Đường dẫn gốc của project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from sqlalchemy.orm import Session
from src.app.utils.supabase import SessionLocal
from src.app.model import Role, User


def seed_data():
    db: Session = SessionLocal()
    
    try:
        roles_data = [
            { "name": "User", "description": "Người dùng thông thường"},
            { "name": "Admin", "description": "Quản trị viên hệ thống"},
        ]
        
        for r_data in roles_data:
            existing_role = db.query(Role).filter(Role.name == r_data["name"]).first()
            if not existing_role:
                new_role = Role(**r_data)
                db.add(new_role)
                print(f"✅ Đã tạo Role: {r_data['name']}")
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi khi chèn dữ liệu mẫu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
