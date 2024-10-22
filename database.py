from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async_engine = create_async_engine(
    url='sqlite+aiosqlite:///cryptogame.db'
)

async_session = async_sessionmaker(async_engine)

