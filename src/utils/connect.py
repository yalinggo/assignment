from utils.config import DB_HOST, DB_NAME, DB_C_TASK
import motor.motor_asyncio
import logging

logger = logging.getLogger(__name__)

logger.info(f"Connect DB : {DB_NAME}, DB_c_task: {DB_C_TASK}")


class Database():
    """
    Database init
    """
    def __init__(self):
        self.client = None
        self.db = None
        self.connect_database()

    def connect_database(self):
        try:
            logger.info('Build database connection.')
            # DB 連接
            self.client = motor.motor_asyncio.AsyncIOMotorClient(DB_HOST)
            self.db = self.client[DB_NAME]
            self.tasks_collection = self.db[DB_C_TASK]
            
        # Todo add exception
        except Exception as e:
            logger.error("Database connection failed: %s", e)

    def get_tasks_collection(self):
        return self.tasks_collection