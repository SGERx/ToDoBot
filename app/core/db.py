import functools

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(self, cls):
        return cls.__name__.lower()


Base = declarative_base(cls=PreBase)
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=True,
)

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


def with_async_session(async_session_func):
    """
    Декоратор для передачи асинхронной сессии SQLAlchemy в качестве зависимости
    в функции-обработчики aiogram.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async for session in get_async_session():
                return await func(session, *args, **kwargs)
        return wrapper
    return decorator
