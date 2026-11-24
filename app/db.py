# ORM = Object Relational Mapping
# it prevents you from writing sql or nosql queries and instead
# allows us to write python like code that defines, create and retrieve data etc

from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
import datetime

# sql database python like
DATABASE_URL = "sqlite+aiosqlite:///./test.db" # can switch with live postgre connection link

class Post(DeclarativeBase):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
    # finds all the classes that inherits from DeclarativeBase
    # it starts the engine and it creates them inside the database
        await conn.run_async(DeclarativeBase.metadata.create_all) 
    
    
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
    # allows for access, to write and read from it asyncronosly
        yield session