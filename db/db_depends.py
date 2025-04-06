from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from db.db import async_session_maker
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db() -> AsyncGenerator[Any, Any]:
    async with async_session_maker() as session:
        yield session