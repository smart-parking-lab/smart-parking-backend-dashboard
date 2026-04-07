from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.supabase import SessionLocal


async def get_db():
    db: AsyncSession = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
