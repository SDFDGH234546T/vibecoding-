"""
这个模块目的：封装数据库创建和关闭工具类
"""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from atguigu.conf.config import settings

# 1 定义两个变量
# 引擎对象，执行操作对象
engine: AsyncEngine | None = None
# session会话对象
# sqlalchemy创建数据库会话对象以工厂形式创建
async_session: async_sessionmaker[AsyncSession]

# 2 创建两个方法
# 1 创建上面两个对象
# 异步
def init_db_engine():
    global engine, async_session
    # 创建引擎对象
    engine = create_async_engine(
        # 数据库路径，必须要有
        settings.database_url,
        # 可选 输出底层sql语句
        echo=True,
    )
    # session会话对象  以工厂形式创建
    async_session = async_sessionmaker(
        engine,
    )

# 2 关闭资源
async def close_db_engine():
    await engine.dispose()

# 测试方法
async def test():
    init_db_engine()
    # 写法特殊：固定的
    async with async_session() as session:
        result = await session.execute(text("select 1"))
        print(result.fetchone())
    await close_db_engine()

if __name__ == '__main__':
    asyncio.run(test())


