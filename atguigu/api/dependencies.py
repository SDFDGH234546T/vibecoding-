from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.repository.dialogue_repository import DialogueRepository
from atguigu.service.dialogue_service import DialogueService
from atguigu.utils import db


# 创建获取数据库操作session对象方法
async def get_session():
    async with db.async_session() as session:
        yield session

# 创建repository对象
async def get_repository(session:AsyncSession=Depends(get_session)):
    return DialogueRepository(
        session=session,
    )

# 创建engine对象
async def get_engine():
    return DialogueEngine()

async def get_dialogue_service(
        repository:DialogueRepository=Depends(get_repository),
        engine:DialogueEngine=Depends(get_engine)):
    return DialogueService(
        repository=repository,
        engine=engine,
    )