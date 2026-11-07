"""
创建路由
"""
import uuid

from fastapi import APIRouter, Depends

from atguigu.api.dependencies import get_dialogue_service
from atguigu.api.schemas import ChatRequest, ChatResponse, ChatMessage
from atguigu.service.dialogue_service import DialogueService

chat_router = APIRouter()

@chat_router.post("/api/chat")
async def chat(chat_request:ChatRequest,
       dialogue_service:DialogueService=Depends(get_dialogue_service)):
    # 1 接收前端提交过来的数据
    ## fastapi封装
    # 2 调用service方法实现
    # service = DialogueService()
    # service.test()

    # todo 返回模拟数据，流程跑通
    return ChatResponse(
        sender_id=chat_request.sender_id,
        message_id=str(uuid.uuid4()),
        messages=[ChatMessage(
            text="hello",
            object=None
        )],
    )
