from fastapi import Depends

from atguigu import repository
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.repository.dialogue_repository import DialogueRepository
from atguigu.service.dialogue_service import DialogueService


# 创建repository对象
async def get_repository():
    # todo 注入操作数据库session会话对象
    return DialogueRepository()

# 创建engine对象
async def get_engine():
    return DialogueEngine()

async def get_dialogue_service():
    return DialogueService(
        repository=Depends(get_repository),
        engine=Depends(get_engine),
    )