import json

import pika

from xprint import xprint


class ShoppingEventProducer:

    def __init__(self):
        # Do not edit the init method.
        # Set the variables appropriately in the methods below.
        self.connection = None
        self.channel = None

    def initialize_rabbitmq(self):
        # To implement - Initialize the RabbitMq connection, channel, exchange and queue here
        xprint("ShoppingEventProducer initialize_rabbitmq() called")

    def publish(self, shopping_event):
        xprint("ShoppingEventProducer: Publishing shopping event {}".format(vars(shopping_event)))
        # To implement - publish a message to the Rabbitmq here
        # Use json.dumps(vars(shopping_event)) to convert the shopping_event object to JSON

    def close(self):
        # Do not edit this method
        self.channel.close()
        self.connection.close()
