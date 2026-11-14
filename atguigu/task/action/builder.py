"""
这个模块 把所有action注册到字典里面 方法
"""
from atguigu.task.action.custom.logistics_tracking import LogisticsTrackingAction
from atguigu.task.action.custom.order_status_query import OrderStatusAction
from atguigu.task.action.registry import ActionRegistry

# 注册action方法
def register_action(action_registry:ActionRegistry):
    action_registry.register(LogisticsTrackingAction())
    action_registry.register(OrderStatusAction())

# todo 根据包扫描机制自动注册