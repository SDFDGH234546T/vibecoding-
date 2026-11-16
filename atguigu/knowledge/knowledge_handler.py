"""
这个模块作用 作为知识检索入口
"""
from atguigu.domain.message import BotMessage, UserMessage
from atguigu.domain.state import DialogueState
from atguigu.knowledge.intents import KNOWLEDGE_INTENTS
from atguigu.knowledge.provider import KnowledgeProvider, KnowledgeChunk
from atguigu.knowledge.registry import KnowledgeProviderRegistry
from atguigu.knowledge.responder import KnowledgeResponder


class KnowledgeHandler:
    def __init__(self,knowledge_registry:KnowledgeProviderRegistry,
                 knowledge_responder:KnowledgeResponder):
        self.knowledge_registry = knowledge_registry
        self.knowledge_responder = knowledge_responder

    # 1 获取llm意图识别到知识检索值  list[str]
    ##  ["product_info","refund_policy","return_policy"]

    # 2 根据意图识别值到知识检索范围字典获取对应答案位置
    # 找到对应的 provider_ids 值，list[str],去重
    ## ["api.product","faq.default", "rag.default"]

    # 3 根据找到答案位置值 provider_ids，到字典找到对应provider对象

    # 4 执行对应provider对象远程调用方法，得到远程调用中台接口结果

    # 5 把调用中台接口得到结果调用模块，提交llm修改，最终返回用户

    # knowledge_intents: 意图识别结果值
    async def handle(self,
                     knowledge_intents:list[str],
                     state:DialogueState,
                     user_message:UserMessage)->list[BotMessage]:
        # 1 获取llm意图识别到知识检索值  knowledge_intents list[str]
        ##  ["product_info","refund_policy","return_policy"]

        # 2 根据意图识别值到知识检索范围字典获取对应答案位置
        # 找到对应的 provider_ids 值，list[str],去重
        ## ["api.product","faq.default", "rag.default"]
        provider_ids:list[str] = self.get_provider_ids(knowledge_intents)

        # 3 根据找到答案位置值 provider_ids，到字典找到对应provider对象
        # 4 执行对应provider对象远程调用方法，得到远程调用中台接口结果
        ## ["api.product","faq.default", "rag.default"]
        final_result:list[KnowledgeChunk] = []
        for provider_id in provider_ids:
            provider_obj:KnowledgeProvider = (
                      self.knowledge_registry.get_provider(provider_id))
            # 调用provider的方法实现远程调用
            result:list[KnowledgeChunk] = await provider_obj.execute(
                state=state,
                user_message=user_message,
            )
            # 每次调用结果合并到final_result
            final_result.extend(result)

        # 5 把调用中台接口得到结果调用模块，提交llm修改，最终返回用户
        bot_message:BotMessage = await self.knowledge_responder.respond(
            chunks=final_result,
            state=state,
            user_message=user_message,
        )
        return [bot_message]

    # 根据意图识别值到知识检索范围字典获取对应答案位置
    # 意图识别结果：["product_info","refund_policy","return_policy"]
    #                      |
    ## 答案位置：  ["api.product","faq.default", "rag.default"]
    def get_provider_ids(self,
                knowledge_intents:list[str])->list[str]:
        final_provider_ids:list[str]=[]
        # 遍历意图识别结果列表
        for intent in knowledge_intents:
            # 拿着遍历之后每个intent到字典找到对应 provider_ids
            final_provider_ids.extend(KNOWLEDGE_INTENTS[intent].provider_ids)

        # final_provider_ids去重
        # 第一种 set集合，缺陷：无法保证列表数据顺序
        return list(set(final_provider_ids))

        # 第二种 dict方法 dict.fromkeys(), 可以去重，可以保证列表数据顺序
        # return dict.fromkeys(final_provider_ids)