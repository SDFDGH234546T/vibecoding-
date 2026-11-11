
from atguigu.domain.state import TaskInstance, DialogueState
from atguigu.plan.command import StartFlowCommand, ResumeTaskCommand, CancelTaskCommand
from atguigu.prompts.models import TurnPlan, TurnPlanValidationResult, ClarifyReason, TaskTurnPlan
from atguigu.task.flow.models import FlowCatalog

"""
这个模块作用：对llm意图识别结果进行校验
"""
class TurnPlanValidator:
    def validate(self,
                 turn_plan:TurnPlan,
                 state:DialogueState,
                 flow_catelog:FlowCatalog)->TurnPlanValidationResult:
        # 对意图识别校验校验：
        active_tracks:list[str] = []
        # 判断
        if turn_plan.task is not None:
            active_tracks.append("task")
        if turn_plan.knowledge is not None:
            active_tracks.append("knowledge")
        if turn_plan.chitchat is not None:
            active_tracks.append("chitchat")

        ## 1 是否识别到内容
        if not active_tracks:
            return TurnPlanValidationResult(
                valid=False,
                reason=ClarifyReason.MISSING_TRACK
            )
        ## 2 识别方向是否是多个
        if len(active_tracks) > 1:
            return TurnPlanValidationResult(
                valid=False,
                reason=ClarifyReason.MULTIPLE_TRACKS
            )

        # 3 如果识别一个方向，根据方向类型做不同校验
        active_track = active_tracks[0]
        if active_track == "task": # 任务流程校验
            return self._validate_task(
                turn_plan.task,
                state,
                flow_catelog
            )
        if active_track == "knowledge": # 知识检索校验
            return self._validate_knowledge()

        return TurnPlanValidationResult(valid=True)

    # 任务流程校验
    def _validate_task(self,task:TaskTurnPlan,
                       state:DialogueState,
                       flow_catelog:FlowCatalog
                        )->TurnPlanValidationResult:
        if not task.commands:
            return TurnPlanValidationResult(valid=False,
                                            reason=ClarifyReason.MISSING_TASK_COMMANDS)

        # 获取commands列表，遍历，得到每个command，根据类型不同校验
        for command in task.commands:
            # start_flow
            if isinstance(command, StartFlowCommand):
                # 获取flow
                flow_id = command.flow
                # 判断flow_id在yaml文件是否存在
                if flow_id not in flow_catelog.flows:
                    return TurnPlanValidationResult(
                        valid=False,
                        reason=ClarifyReason.INVALID_TASK_COMMAND
                    )

            # resume_task
            # 恢复任务，前提条件：要暂停任务才可以恢复，在暂停列表有要恢复任务
            if isinstance(command, ResumeTaskCommand):
                # 把中断列表所有任务id获取出来 构建新列表
                ## [1,2,3,4]
                paused_task_id = [paused_task.task_id
                    for paused_task in state.tasks.paused
                ]
                # 获取意图识别task_id
                task_id = command.task_id
                if task_id not in paused_task_id:
                    return TurnPlanValidationResult(
                        valid=False,
                        reason=ClarifyReason.INVALID_TASK_COMMAND
                    )

            # cancel_task
            # 拿着识别要取消任务id 到两个地方找是否存在
            ## 中断列表    当前活跃任务
            if isinstance(command, CancelTaskCommand):
                # 1 从中断列表获取所有任务id，新列表
                all_task_id = [paused_task.task_id
                    for paused_task in state.tasks.paused
                ]

                # 2 从当前活跃任务获取任务id，放到上面列表
                if state.tasks.active:
                    all_task_id.append(state.tasks.active.task_id)

                # 3 判断
                if command.task_id not in all_task_id:
                    return TurnPlanValidationResult(
                        valid=False,
                        reason=ClarifyReason.INVALID_TASK_COMMAND
                    )

        return TurnPlanValidationResult(valid=True)

    def _validate_knowledge(self):
        return TurnPlanValidationResult(valid=True)