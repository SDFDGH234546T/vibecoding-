"""
这个模块类型TaskHandler里面action
发送远程调用，调用中台接口得到数据
"""
import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from atguigu.conf.config import settings
from atguigu.domain.message import UserMessage
from atguigu.domain.state import DialogueState
from atguigu.task.action.base import ActionResult
from atguigu.task.task_handler import TaskHandler
from atguigu.utils import httpx_client


# 定义类封装最终结果
@dataclass
class KnowledgeChunk:
    content: str = ""

# 创建基类，定义属性和抽象方法
class KnowledgeProvider(ABC):
    # 属性
    provider_id:str=""

    # 抽象方法
    @abstractmethod
    async def execute(self,state:DialogueState,
                      user_message:UserMessage) -> list[KnowledgeChunk]:
        pass

# 商品信息咨询
class ApiProductProvider(KnowledgeProvider):
    provider_id="api.product"

    # 远程调用
    async def execute(self,state:DialogueState,
                      user_message:UserMessage) -> list[KnowledgeChunk]:
        # 获取商品id
        product_id = state.shared.focused_object.id
        # 远程调用
        url = f"{settings.commerce_api_base_url}/products/{product_id}"
        response = await httpx_client.http_client.get(url)
        data = response.json().get("data",{})
        chunk = json.dumps(data, ensure_ascii=False)
        return [KnowledgeChunk(content=chunk)]

# 订单信息咨询  api.order
class ApiOrderProvider(KnowledgeProvider):
    provider_id = "api.order"

    async def execute(self, state: DialogueState,
                      user_message: UserMessage) -> list[KnowledgeChunk]:
        order_id = state.shared.focused_object.id
        # 拼接远程调用路径
        # 得到订单信息，调用两个中台接口
        # 调用查询订单详情接口
        order_url = f"{settings.commerce_api_base_url}/orders/{order_id}"
        # 调用查询订单物流接口
        logis_url = f"{settings.commerce_api_base_url}/orders/{order_id}/logistics"
        # 远程调用，因为两个接口需要调用，使用并行方式实现
        ## 返回结果和传入参数顺序相关的
        order_info,logis_info = await asyncio.gather(
            httpx_client.http_client.get(order_url),
            httpx_client.http_client.get(logis_url)
        )

        # list[KnowledgeChunk]
        chunk = json.dumps({
            "order_detail": order_info.json()["data"],
            "logis_detail": logis_info.json()["data"],
        }, ensure_ascii=False
        )
        return [KnowledgeChunk(content=chunk)]

# 5 faq
## 查询固定问题和固定答案
# 把这些问题和对应答案存储数据库里面，使用mysql，向量数据库
# 根据问题到数据库找到匹配问题，返回问题对应答案
class FAQProvider(KnowledgeProvider):
    provider_id = 'faq.default'

    async def execute(self, state: DialogueState,
                      user_message: UserMessage) -> list[KnowledgeChunk]:
        # TODO
        return [KnowledgeChunk(content="未检索到相关问题")]


# rag
## 调用智库里面查询接口得到结果
class RAGProvider(KnowledgeProvider):
    provider_id = 'rag.default'

    async def execute(self, state: DialogueState,
                      user_message: UserMessage) -> list[KnowledgeChunk]:
        # RAG知识库查询知识接口（TODO）
        return [KnowledgeChunk(content="未检索到相关信息")]