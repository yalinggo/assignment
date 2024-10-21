from model.doa import Task
from model.rabbitmq import Taskqueue
from utils.status import format_response
import asyncio
import logging
import aio_pika

logger = logging.getLogger(__name__)


class TaskController():
    def __init__(self, db):
        self.task_model = Task(db)
        self.task_queue = Taskqueue()

    async def create_task(self, msg):
        task_data = await self.task_model.create_task(msg)
        task_id = task_data['task_id']
        await self.task_queue.publish_task("src_task", task_id)
        return task_data

    async def cancel_task(self, task_id):
        task = await self.task_model.get_task_by_id(task_id)
        if not task:
            return format_response(status_code=404, message="Task not found.")
        if task['status'] in ['processing', 'pending']:
            await self.task_model.cancel_task(task_id)
            logger.info(f"Task {task_id} was cancelled.")
            return format_response(status_code=200, err_code="Success")
        return format_response(status_code=400, err_code="The task has been processed, it cannot be cancelled.")
    
    async def get_all_tasks(self):
        tasks = await self.task_model.get_all_tasks()
        return tasks
    
    async def push_data(self, task_id, status):
        try:
            if status == 'cancelled':
                logger.info(f"Task {task_id} was cancelled and published to dst_task queue..")
                data = f"Cancelled {task_id}"
            else:
                logger.info(f"Task {task_id} processed and published to dst_task queue.")
                data = f"Processed {task_id}"
            await self.task_queue.publish_task('dst_task', data)
        except Exception as e:
             logger.error(e)

    async def process_task(self, task_id):
        try:
            task = await self.task_model.get_task_by_id(task_id)
            if task:
                if task['status'] == "cancelled":
                    await self.push_data(task_id, task['status'])
                    return
                
                await self.task_model.process_task(task_id)
                # 模擬處理三秒
                await asyncio.sleep(3)

                # 在處理的過程中再檢查一次任務狀態，避免已取消的任務繼續處理
                task_check = await self.task_model.get_task_by_id(task_id)
                if task_check and task_check['status'] == 'cancelled':
                    await self.push_data(task_id, task_check['status'])
                    return
                
                await self.task_model.finish_task(task_id)
                # push completed data to dst_task queue
                await self.push_data(task_id, task_check['status'])
                
        except Exception as e:
            logger.error(e)

    async def callback(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                task_id = message.body.decode()
                logger.info(f"Received task {task_id} from src_task queue.")
                await self.process_task(task_id)
            except Exception as e:
                logger.error(e)

    async def start_consumer(self):
        try:
            channel = await self.task_queue.get_rabbitmq_channel()
            logger.info("Channel created.")
            queue = await channel.declare_queue('src_task', durable=True)
            logger.info("Queue declared.")
            await queue.consume(self.callback)
            logger.info("Consumer started and waiting for messages from src_task queue...")
        except Exception as e:
            logger.error("Error in starting consumer: %s", e)

