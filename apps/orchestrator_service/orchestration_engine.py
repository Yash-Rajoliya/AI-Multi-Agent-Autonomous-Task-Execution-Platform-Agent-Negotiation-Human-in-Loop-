from infrastructure.messaging.message_bus import KafkaBus
from infrastructure.messaging.event_schema import BaseEvent, EventMetadata
from .workflow_compiler import WorkflowCompiler
from .state_manager import StateManager


class OrchestrationEngine:
    def __init__(self, bus: KafkaBus):
        self.bus = bus
        self.compiler = WorkflowCompiler()
        self.state = StateManager()

    async def handle_task_created(self, event: BaseEvent):
        task_id = event.payload["task_id"]

        # Compile workflow DAG
        workflow = self.compiler.compile(event.payload)

        # Save state
        await self.state.create_workflow(task_id, workflow)

        # Emit event
        new_event = BaseEvent(
            metadata=EventMetadata(
                event_type="workflow.compiled",
                source="orchestrator",
                trace_id=event.metadata.trace_id,
            ),
            payload={
                "task_id": task_id,
                "workflow": workflow.dict(),
            },
        )

        await self.bus.publish("workflow.compiled.v1", new_event)