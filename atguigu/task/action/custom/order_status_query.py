"""
这个模块远程调用中台接口查询订单状态信息
"""
from atguigu.conf.config import settings
from atguigu.domain.state import DialogueState
from atguigu.task.action.base import Action, ActionResult
from atguigu.utils import httpx_client


class OrderStatusAction(Action):
    name = "action_lookup_order_status"

    async def run(self,state:DialogueState) -> ActionResult:
        order_number = state.tasks.active.slots.get("order_number")
        url = f"{settings.commerce_api_base_url}/orders/{order_number}/status"
        response = await httpx_client.http_client.get(url)
        data = response.json().get("data")
        return ActionResult(
            slots_update={
                "order_status": data.get("status"),
                "order_summary": data.get("status_desc"),
            }
        )
