from dotenv import load_dotenv
import os


load_dotenv()

# Load environment variables
# DB
DB_HOST = os.getenv("DB_HOST", "mongodb+srv://test:test@cluster0.jtr0rvw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "task_db")
DB_C_TASK = os.getenv("DB_C_TASK", "task")

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '0.0.0.0')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
