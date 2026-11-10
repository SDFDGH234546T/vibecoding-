from pathlib import Path

import yaml

from atguigu.task.flow.models import Flow, FlowCatalog, FlowSlot
from atguigu.task.flow.steps import FlowStep

"""
这个模块作用解析yaml，封装对应对象
"""
class FlowLoader:
    def load(self,path:Path)->FlowCatalog:
        # read_text读取yaml文件内容，读取是字符串
        yaml_text = path.read_text(encoding='utf-8')
        # safe_load把读取字符串解析字典形式
        flow_dict = yaml.safe_load(yaml_text)

        # dict[str, Any]
        # flows: dict[str, Flow]
        # slots: dict[str, FlowSlot]
        #
        return FlowCatalog(flows=None,slots=None)
