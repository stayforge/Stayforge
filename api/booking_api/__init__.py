"""
Stayforge Booking API api_factory

Stayforge Booking API is used for application-level booking_api operations.
"""
from mq import MessageQueue

mq = MessageQueue(stream_name=stream)
mq.enqueue('')
