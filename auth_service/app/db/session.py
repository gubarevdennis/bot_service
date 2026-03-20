# auth_service/app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

engine = create_async_engine(f"sqlite+aiosqlite:///{settings.SQLITE_PATH}", echo=False) 
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    """Dependency, который предоставляет асинхронную сессию."""
    async with AsyncSessionLocal() as session:
        yield session