import warnings
import redis
import settings

# Logger for Redis Queue
logger = settings.getLogger('MQ')


# Custom warning for Redis connection issues
class RedisConnectionWarning(Warning):
    pass


class MessageQueue:
    def redis_connector(self):
        """
        Initialize Redis client using the provided Redis URL.
        """
        return redis.StrictRedis.from_url(self.redis_url)

    def __init__(self, stream_name: str = None):
        """
        Initialize the message queue, Redis connection, and fallback in-memory queue.
        """
        # Define Redis URL from settings
        self.redis_url = settings.REDIS_URL + "stayforge_mq"

        # Initialize Redis client
        self.redis_client = self.redis_connector()
        self.stream_name = stream_name if stream_name else 'task_stream'

        # Test Redis connection
        try:
            self.redis_client.ping()
            self.redis_connected = True
        except redis.exceptions.ConnectionError as e:
            self.redis_connected = False
            logger.error(f"Redis connection failed: {e}")
            warnings.warn(f"Redis connection error: {e}", RedisConnectionWarning)

        # Initialize fallback in-memory queue
        self.queue = []

    def _enqueue(self, message):
        """
        Low-level enqueue operation. Push message into Redis if connected,
        otherwise fallback to in-memory queue.
        """
        if self.redis_connected:
            try:
                self.redis_client.lpush(self.stream_name, message)
                logger.info(f"Message enqueued in Redis: {message}")
            except redis.exceptions.ConnectionError as e:
                logger.error(f"Failed to push message to Redis: {e}")
                self.redis_connected = False
                self.queue.append(message)
        else:
            self.queue.append(message)
            logger.warning(f"Message enqueued in in-memory queue due to Redis disconnection: {message}")

    def _dequeue(self):
        """
        Low-level dequeue operation. Fetch message from Redis if connected,
        otherwise fallback to in-memory queue.
        """
        if self.redis_connected:
            try:
                message = self.redis_client.rpop(self.stream_name)
                if message:
                    logger.info(f"Message dequeued from Redis: {message.decode('utf-8')}")
                return message
            except redis.exceptions.ConnectionError as e:
                logger.error(f"Failed to pop message from Redis: {e}")
                self.redis_connected = False
        # Fallback to in-memory queue
        if self.queue:
            message = self.queue.pop(0)
            logger.warning(f"Message dequeued from in-memory queue: {message}")
            return message
        return None

    def enqueue(self, message):
        """
        Public method to enqueue a message.
        """
        self._enqueue(message)
        logger.debug(f"{self.stream_name} - 'enqueue': {message}")

    def dequeue(self):
        """
        Public method to dequeue a message.
        """
        message = self._dequeue()
        if message:
            logger.debug(f"{self.stream_name} - 'dequeue': {message}")
            return message.decode('utf-8') if isinstance(message, bytes) else message
        logger.debug(f"{self.stream_name} - 'dequeue' returned no message.")
        return None

    def size(self):
        """
        Get the current size of the queue.
        """
        if self.redis_connected:
            try:
                queue_size = self.redis_client.llen(self.stream_name)
                logger.info(f"Queue size in Redis: {queue_size}")
                return queue_size
            except redis.exceptions.ConnectionError as e:
                logger.error(f"Failed to get size from Redis: {e}")
                self.redis_connected = False
        # Fallback to in-memory queue
        queue_size = len(self.queue)
        logger.info(f"Queue size in memory: {queue_size}")
        return queue_size

