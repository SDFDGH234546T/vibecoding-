from pydantic import TypeAdapter

from atguigu.domain.state import DialogueState

"""
这个模块作用：用于操作mysql数据库
"""
# 类型适配器，对象  json字符串互相转换
# json字符串 -- 对象：validate_json()
# 对象 -- json字符串：dump_json()
dialogue_state_adapter = TypeAdapter(DialogueState)

class DialogueRepository:
    # 根据sender_id查询
    async def load_state(self, sender_id):
        pass

    # 保存数据库
    ## 不存在添加，存在更新
    async def save_state(self, state):
        pass