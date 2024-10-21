from dotenv import load_dotenv
import os


load_dotenv()

# Load environment variables
# DB
DB_HOST = os.getenv("DB_HOST", "")
DB_NAME = os.getenv("DB_NAME", "task_db")
DB_C_TASK = os.getenv("DB_C_TASK", "task")

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', '')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', '')

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
WORKERNUM = int(os.getenv("WORKERNUM", "10"))
