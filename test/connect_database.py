from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.app.model.base import Base

from sqlalchemy.pool import NullPool

# Using the same database as production as requested ("test trực tiếp")
DATABASE_URL = "postgresql+asyncpg://postgres.jgxlvshakravvjmdpbml:hethongnhung@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
