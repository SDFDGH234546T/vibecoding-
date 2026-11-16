"""
这个模块 把所有action注册到字典里面 方法
"""
import importlib
import inspect
import pkgutil

from atguigu.task.action.base import Action
from atguigu.task.action.custom.logistics_tracking import LogisticsTrackingAction
from atguigu.task.action.custom.order_status_query import OrderStatusAction
from atguigu.task.action.registry import ActionRegistry

# 注册action方法
def register_action(action_registry:ActionRegistry):
    action_registry.register(LogisticsTrackingAction())
    action_registry.register(OrderStatusAction())

# 根据包扫描机制自动注册
def register_custom_action(action_registry:ActionRegistry):
    # 1 设置找的包路径，到哪个包找到action
    package = importlib.import_module(
           "atguigu.task.action.custom")

    # 2 遍历包所有内容，只需要找到模块 py文件 atguigu.task.action.custom.
    for _,module_name,is_package in pkgutil.iter_modules(
                package.__path__,
                prefix=f"{package.__name__}."):
        # is_package 是True 当前遍历获取包
        if is_package:
            continue

        module = importlib.import_module(module_name)
        # 遍历模块py文件，从模块获取class类   类 属性 方法
        for _,action_class in inspect.getmembers(module,inspect.isclass):
            # 判断 action_class是Action基类子类
            if (
                not issubclass(action_class, Action)
                or action_class is Action
            ):
                continue

            if action_class.__module__ != module.__name__:
                continue

            # 注册
            action_registry.register(action_class())