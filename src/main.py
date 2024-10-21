from controller.task_controller import TaskController
from utils.connect import Database
from utils.status import format_response
from utils.data_structure import CancelTaskRequest, TaskRequest
from utils.config import HOST, PORT, WORKERNUM
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
import uvicorn
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Service Starting up...")
    global controller
    db = Database()
    controller = TaskController(db)
    logger.info("start consumer task")
    # Start the RabbitMQ consumer as a background task
    await controller.start_consumer()
    yield
    logger.info("Service shutting down...")
    await controller.stop_consumer()
    await db.close()

app = FastAPI(lifespan=lifespan)


@app.post("/create_task")
async def create_task(request: TaskRequest):
    resp = await controller.create_task(request)
    return format_response(status_code=200, message=resp)


@app.post("/tasks/cancel")
async def cancel_task(request: CancelTaskRequest):
    resp = await controller.cancel_task(request.task_id)
    return resp


@app.get("/tasks")
async def get_tasks():
    resp = await controller.get_all_tasks()
    return jsonable_encoder(resp)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, workers=WORKERNUM)
