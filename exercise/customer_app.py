from types import SimpleNamespace
import pika
import json
from db_and_event_definitions import ProductEvent, BillingEvent
import time
import logging

from xprint import xprint


class CustomerEventConsumer:

    def __init__(self, customer_id):
        # Do not edit the init method.
        # Set the variables appropriately in the methods below.
        self.customer_id = customer_id
        self.connection = None
        self.channel = None
        self.temporary_queue_name = None
        self.shopping_events = []
        self.billing_events = []

    def initialize_rabbitmq(self):
        # To implement - Initialize the RabbitMq connection, channel, exchange and queue here
        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='customer_app_events', exchange_type='topic')
        result = self.channel.queue_declare('', exclusive=True)
        self.temporary_queue_name = result.method.queue
        self.channel.queue_bind(exchange='customer_app_events', queue=self.temporary_queue_name, routing_key=self.customer_id)

        xprint("CustomerEventConsumer {}: initialize_rabbitmq() called".format(self.customer_id))

    def handle_event(self, ch, method, properties, body):
        # To implement - This is the callback that is passed to "on_message_callback" when a message is received
        event = json.loads(body.decode())
        if 'event_type' in event:
            shopping_event = ProductEvent(event['even_type'], event['product_number'], event['timestamp'])
            self.shopping_events.append(shopping_event)
        else:
            billing_event = BillingEvent(event['customer_id'], event['product_number'], event['pickup_time'], event['purchase_time'], event['shopping_cost'])
            self.billing_events.append(billing_event)
        
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        xprint("CustomerEventConsumer {}: handle_event() called".format(self.customer_id))

    def start_consuming(self):
        # To implement - Start consuming from Rabbit
        self.channel.basic_consume(queue=self.temporary_queue_name, on_message_callback=self.handle_event)
        self.channel.start_consuming()
        xprint("CustomerEventConsumer {}: start_consuming() called".format(self.customer_id))

    def close(self):
        # Do not edit this method
        try:
            if self.channel is not None:
                print("CustomerEventConsumer {}: Closing".format(self.customer_id))
                self.channel.stop_consuming()
                time.sleep(1)
                self.channel.close()
            if self.connection is not None:
                self.connection.close()
        except Exception as e:
            print("CustomerEventConsumer {}: Exception {} on close()"
                    .format(self.customer_id, e))
            pass
