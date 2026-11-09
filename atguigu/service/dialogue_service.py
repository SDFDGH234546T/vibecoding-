"""
这个模块是service业务逻辑层，负责调用其他层实现
调用repository操作数据库
调用engine处理消息
"""
from atguigu.domain.message import UserMessage, ProcessResult
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.repository.dialogue_repository import DialogueRepository


class DialogueService:

    def __init__(self, repository: DialogueRepository,
                      engine: DialogueEngine):
        self.repository = repository
        self.engine = engine


    async def run(self, user_message:UserMessage)->ProcessResult:
        # 1 注入要调用层对象，repository对象（操作数据库） 和 engine对象（处理消息）
        # 2 根据sender_id获取当前用户历史消息处理数据

        # 3 调用engine层方法处理当前消息

        # 4 把处理消息之后最新处理数据保存数据库里面

        # 5 返回engine处理结果
        pass