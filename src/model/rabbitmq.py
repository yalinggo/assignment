from utils.config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD
import aio_pika
import logging
import asyncio

logger = logging.getLogger(__name__)


class Taskqueue():
    """
    任務推送管理
    """
    def __init__(self):
        self.connection = None
        self.channel = None
        self.connection_url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/'
        
    async def initialize(self):
        asyncio.create_task(self.connect_rabbitmq())
        
    async def publish_task(self, queue_name, task_id):
        if not self.channel or not self.connection:
            await self.connect_rabbitmq()
        # Declare the queue
        queue = await self.channel.declare_queue(queue_name, durable=True)
        # Publish the message
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=task_id.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue.name,
        )
        logger.info(f"Task {task_id} published to RabbitMQ queue: {queue_name}.")

    async def connect_rabbitmq(self):
        retry_interval = 5  
        max_retries = 5  
        retry_count = 0
        while retry_count < max_retries:
            try:
                logger.info('Building RabbitMQ connection...')
                # Build RabbitMQ connection URL using environment variables
                self.connection = await aio_pika.connect_robust(self.connection_url)
                # Creating a channel
                self.channel = await self.connection.channel()
                await self.channel.set_qos(prefetch_count=1)
                logger.info("RabbitMQ connection established.")
                return
            except aio_pika.exceptions.AMQPConnectionError:
                retry_count += 1
                logger.error(f"RabbitMQ connection failed. Retrying in {retry_interval} seconds... ({retry_count}/{max_retries})")
                await asyncio.sleep(retry_interval)

        logger.error("RabbitMQ connection failed after maximum retries. Please check RabbitMQ status.")

    async def get_rabbitmq_channel(self):
        if self.connection and self.connection.is_closed:
            logger.info("RabbitMQ connection lost, reconnecting...")
            await self.connect_rabbitmq()
        if not self.channel or self.channel.is_closed:
            logger.info("RabbitMQ channel lost or not established, reconnecting...")
            await self.connect_rabbitmq()
        return self.channel