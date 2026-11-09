from atguigu.domain.message import UserMessage, ProcessResult, BotMessage
from atguigu.domain.state import DialogueState

"""
这个模块作用：用于处理消息
"""
class DialogueEngine:
    async def process_message(self,
                    state:DialogueState,
                              user_message:UserMessage)->ProcessResult:
        # 1 准备 session
        ## 获取当前session
        ### 如果获取不到，创建新session
        ### 如果获取到，判断session是否过期（60分钟不活跃）
        ####          如果没有过期，使用当前session
        ####          如果session过期，创建新的session，清空过期session任务

        # 2 封装一轮对象 （用户提问）

        # 3 判断消息类型：文本 或者 对象类型消息

        # 3.1 如果消息：文本类型
        ## * 使用llm意图识别：识别文本执行哪个能力：任务流程、知识检索、闲聊
        ##                   如果识别任务流程，流程id识别到

        ## * 对llm意图识别结果校验，保证正常往后执行
        ### 识别能力最多一个，流程id在yaml文件是否存在......

        ## * 校验失败，执行澄清回复组件

        ## * 校验成功，根据识别方向，调用不同方向处理器

        # 4 封装处理结果，返回用户

        # 3.2 如果对象类型消息
        ## * 封装到focused_object对象里面
        ## * 判断当前执行任务里面是否有可以匹配槽位数据
        ## * 如果没有匹配，执行 澄清回复
        ## * 可以匹配，从对象消息获取数据，执行后续流程

        # 返回模拟数据，为了测试
        return ProcessResult(
            sender_id = user_message.sender_id,
            message_id = user_message.message_id,
            messages=[
                BotMessage(
                    text="hello",
                    object=None
                )
            ]
        )