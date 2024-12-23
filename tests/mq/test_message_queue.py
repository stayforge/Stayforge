import pytest
import fakeredis  # Use fakeredis to simulate Redis
from mq import MessageQueue, RedisConnectionWarning


def test_enqueue_dequeue_redis():
    """
    Test enqueue and dequeue operations when Redis is available.
    """
    # Use fakeredis to simulate Redis
    fake_redis = fakeredis.FakeStrictRedis()

    # Replace redis_url with fakeredis instance
    mq = MessageQueue()
    mq.redis_client = fake_redis
    mq.redis_connected = True  # Simulate Redis connection being active

    # Test enqueue
    mq.enqueue("test_message")
    assert fake_redis.llen("task_stream") == 1  # Verify message is added to Redis queue

    # Test dequeue
    message = mq.dequeue()
    assert message == "test_message"
    assert fake_redis.llen("task_stream") == 0  # Verify Redis queue is empty

    # Test size()
    fake_redis.lpush("task_stream", "another_message")
    assert mq.size() == 1  # Verify queue size


def test_enqueue_dequeue_in_memory_queue():
    """
    Test in-memory queue behavior when Redis is unavailable.
    """
    # Create a MessageQueue instance simulating Redis being unavailable
    mq = MessageQueue()
    mq.redis_client = None
    mq.redis_connected = False

    # Test enqueue (in-memory)
    mq.enqueue("test_message")
    assert mq.queue == ["test_message"]

    # Test dequeue (in-memory)
    message = mq.dequeue()
    assert message == "test_message"
    assert len(mq.queue) == 0  # Ensure in-memory queue is cleared

    # Test size()
    assert mq.size() == 0


def test_fallback_enqueue_after_redis_failure():
    """
    Test automatic fallback to in-memory queue when Redis fails.
    """
    # Use fakeredis to simulate Redis
    fake_redis = fakeredis.FakeStrictRedis()

    # Initialize Redis as connected
    mq = MessageQueue()
    mq.redis_client = fake_redis
    mq.redis_connected = True

    # Simulate Redis connection loss
    mq.redis_connected = False

    # Test enqueue (fallback)
    mq.enqueue("message_after_failure")
    assert mq.queue == ["message_after_failure"]  # Verify fallback to in-memory queue

    # Test dequeue (fallback)
    message = mq.dequeue()
    assert message == "message_after_failure"
    assert len(mq.queue) == 0


def test_redis_connection_warning():
    """
    Test if correct warning is issued when Redis cannot connect.
    """
    # pytest.warns to detect warning
    with pytest.warns(RedisConnectionWarning, match="Redis connection error:"):
        mq = MessageQueue()  # Create MessageQueue instance
    assert mq.redis_connected is False  # Verify Redis connection state


def test_memory_based_queue_operations():
    """
    Test memory-based queue behavior when Redis is not available.
    """
    # Simulate Redis being unavailable, create a MessageQueue instance
    mq = MessageQueue()
    mq.redis_client = None
    mq.redis_connected = False

    # Test enqueue operation (store to in-memory queue)
    mq.enqueue("memory_queue_test_message_1")
    mq.enqueue("memory_queue_test_message_2")
    assert mq.queue == ["memory_queue_test_message_1", "memory_queue_test_message_2"]

    # Test dequeue operation (retrieve from in-memory queue)
    message1 = mq.dequeue()
    assert message1 == "memory_queue_test_message_1"  # Ensure correct message is retrieved from the queue
    assert mq.queue == ["memory_queue_test_message_2"]  # Verify remaining elements in the in-memory queue

    message2 = mq.dequeue()
    assert message2 == "memory_queue_test_message_2"
    assert len(mq.queue) == 0  # Ensure in-memory queue is cleared

    # Test size() method
    assert mq.size() == 0
    mq.enqueue("memory_queue_test_message_3")
    assert mq.size() == 1  # Verify queue size is correctly tracked as messages are added
