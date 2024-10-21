from datetime import datetime
import uuid


class Task():
    """
    處理任務資料讀寫
    """
    def __init__(self, db):
        self.db = db
        self.tasks_collection = self.db.get_tasks_collection()

    async def create_task(self):
        task_id = str(uuid.uuid4())
        task_data = {
            "task_id": task_id,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        await self.tasks_collection.insert_one(task_data.copy())

        return task_data

    async def get_task_by_id(self, task_id):
        return await self.tasks_collection.find_one({"task_id": task_id})

    async def cancel_task(self, task_id):
        await self.tasks_collection.update_one({"task_id": task_id}, {"$set": {"status": "cancelled", "updated_at": datetime.utcnow()}})

    async def process_task(self, task_id):
        await self.tasks_collection.update_one({"task_id": task_id}, {"$set": {"status": "processing", "updated_at": datetime.utcnow()}})

    async def finish_task(self, task_id):
        await self.tasks_collection.update_one({"task_id": task_id}, {"$set": {"status": "completed", "updated_at": datetime.utcnow()}})

    async def get_all_tasks(self):
        tasks = await self.tasks_collection.find().to_list(None)
        rsl = [{k: v for k, v in task.items() if k != '_id'} for task in tasks]
        return rsl