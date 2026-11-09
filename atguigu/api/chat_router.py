"""
创建路由
"""
import uuid
from dataclasses import asdict

from fastapi import APIRouter, Depends

from atguigu.api.dependencies import get_dialogue_service
from atguigu.api.schemas import ChatRequest, ChatResponse, ChatMessage, ChatObject
from atguigu.domain.message import UserMessage, ProcessResult, MessageType, MessageObject
from atguigu.service.dialogue_service import DialogueService

chat_router = APIRouter()


@chat_router.post("/api/chat")
async def chat(chat_request:ChatRequest,
       dialogue_service:DialogueService=Depends(get_dialogue_service)
                                    )->ChatResponse:
    # 1 chat_request 封装前端提交过来的数据
    ## fastapi封装
    # 2 注入service对象
    # Depends
    # 3 调用service方法实现

    # 1 数据模型转换过程
    # 调用service方法，把api层数据模型 转换 service层数据模型
    # ChatRequest -->  UserMessage
    user_message:UserMessage = _build_user_message(chat_request)

    # 2 调用service方法实现
    process_result:ProcessResult = await dialogue_service.run(user_message)

    # 3 把service层返回数据 ProcessResult --> api层类型 ChatResponse
    chat_response:ChatResponse = _build_response_message(process_result)
    return chat_response

    # 返回模拟数据，流程跑通
    # return ChatResponse(
    #     sender_id=chat_request.sender_id,
    #     message_id=str(uuid.uuid4()),
    #     messages=[ChatMessage(
    #         text="hello",
    #         object=None
    #     )],
    # )

# 调用service方法，把api层数据模型 转换 service层数据模型
    # ChatRequest -->  UserMessage
def _build_user_message(chat_request:ChatRequest)->UserMessage:
    return UserMessage(
        sender_id=chat_request.sender_id,
        # 消息id，判断存在使用，不存在生成
        message_id=chat_request.message_id
               if chat_request.message_id else str(uuid.uuid4()),
        type=MessageType.TEXT if chat_request.text
                              else MessageType.OBJECT,
        text=chat_request.text,
        object=MessageObject(
            id=chat_request.object.id,
            type=chat_request.object.type,
            title=chat_request.object.title,
            attributes=chat_request.object.attributes,
        ) if chat_request.object else None
    )


# 3 把service层返回数据 ProcessResult --> api层类型 ChatResponse
# ProcessResult -->  ChatResponse
def _build_response_message(process_result:ProcessResult)->ChatResponse:
    # list[BotMessage] --》 list[ChatMessage]
    return ChatResponse(
        sender_id=process_result.sender_id,
        message_id=process_result.message_id,
        messages=[
            # ChatMessage对象
            ChatMessage(
                text=bot_message.text,
                object=ChatObject(
                    **asdict(bot_message.object)
                ) if bot_message.object else None
            )
            for bot_message in process_result.messages
        ]
    )