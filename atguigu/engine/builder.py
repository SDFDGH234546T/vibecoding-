"""
维护engine层注入关系
"""
from pathlib import Path

from atguigu.chitchat import chit_chat
from atguigu.chitchat.chit_chat import ChitChatHandler
from atguigu.clarify.clarify_response import ClarifyResponse
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.knowledge.knowledge_handler import KnowledgeHandler
from atguigu.knowledge.provider import ApiProductProvider, ApiOrderProvider, FAQProvider, RAGProvider
from atguigu.knowledge.registry import KnowledgeProviderRegistry
from atguigu.knowledge.responder import KnowledgeResponder
from atguigu.plan.turn_plan_validator import TurnPlanValidator
from atguigu.plan.turn_planner import TurnPlanner
from atguigu.task.action.action_runner import ActionRunner
from atguigu.task.action.builder import register_action, register_custom_action
from atguigu.task.action.registry import ActionRegistry
from atguigu.task.command.command_processor import CommandProcessor
from atguigu.task.flow.loader import FlowLoader
from atguigu.task.flow.models import FlowCatalog
from atguigu.task.flowexecutor.flow_executor import FlowExecutor
from atguigu.task.response.response_render import ResponseRender
from atguigu.task.task_handler import TaskHandler
from atguigu.task.tasklifecycle.task_lifecycle import TaskLifecycleResponder


def build_engine()->DialogueEngine:

    # 创建FlowCatalog对象
    flow_path = Path(__file__).parents[2]/'flow_config'/'user_flows.yml'
    flow_catalog:FlowCatalog =FlowLoader().load(flow_path)

    # 意图识别对象
    turn_planner = TurnPlanner()
    # 校验
    turn_plan_validator = TurnPlanValidator()

    # 任务流程
    command_processor = CommandProcessor()
    task_lifycycle = TaskLifecycleResponder(
        flow_catalog=flow_catalog,
    )

    response_render = ResponseRender()
    action_registry = ActionRegistry()
    # 调用方法，把所有action注册
    # register_action(action_registry=action_registry,)
    register_custom_action(action_registry=action_registry,)

    action_runner = ActionRunner(action_registry=action_registry,)

    flow_executor = FlowExecutor(
        response_render=response_render,
        action_runner=action_runner,
    )
    task_handler = TaskHandler(
        command_processor=command_processor,
        task_lifecycle=task_lifycycle,
        flow_catalog=flow_catalog,
        flow_executor=flow_executor,
    )

    chit_chat = ChitChatHandler()
    clarify_response = ClarifyResponse()

    knowledge_registry = KnowledgeProviderRegistry(
        provider_objects=[
            ApiProductProvider(),
            ApiOrderProvider(),
            FAQProvider(),
            RAGProvider()
        ]
    )

    knowledge_handler = KnowledgeHandler(
        knowledge_responder=KnowledgeResponder(),
        knowledge_registry=knowledge_registry
    )
    return DialogueEngine(
        turn_planner=turn_planner,
        turn_plan_validator=turn_plan_validator,
        task_handler=task_handler,
        chit_chat=chit_chat,
        clarify_response=clarify_response,
        knowledge_handler=knowledge_handler
    )