"""
Stayforge Booking API v1

Stayforge Booking API is used for application-level booking_api operations.
"""
from mq import MessageQueue

mq = MessageQueue(stream_name=stream)
mq.enqueue('')
