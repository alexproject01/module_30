from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./cookbook.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(  # type: ignore
    engine, expire_on_commit=False, class_=AsyncSession
)
session = async_session()
Base = declarative_base()
