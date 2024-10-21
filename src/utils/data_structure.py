from pydantic import BaseModel, Field


class CancelTaskRequest(BaseModel):
    task_id: str = Field(..., description="Task unique ID.", examples="e3e6d9f3-2361-4d00-ab22-4099941654c4")