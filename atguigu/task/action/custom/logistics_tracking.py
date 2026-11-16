"""
这个模块远程调用中台物流接口
"""
from atguigu.conf.config import settings
from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.utils import httpx_client


class LogisticsTrackingAction(Action):
    # name属性
    # 和yaml文件查询物流流程action步骤action属性值相同
    name = "action_lookup_logistics"

    # 实现基类里面抽象方法 run
    # 使用httpx实现远程调用
    async def run(self,state:DialogueState) -> ActionResult:
        # 获取需要订单编号
        order_number = state.tasks.active.slots.get("order_number")
        # 拼接远程调用路径
        url = f"{settings.commerce_api_base_url}/orders/{order_number}/logistics"
        # 远程调用httpx
        response = await httpx_client.http_client.get(url)

        # 把远程调用返回数据封装到ActionResult对象里面
        data = response.json().get("data", {})

        return ActionResult(
            slots_update={
                "logistics_company": data.get("logistics_company","未知"),
                "tracking_number": data.get("tracking_number","未知"),
                "logistics_status": data.get("status_desc","未知"),
            }
        )



