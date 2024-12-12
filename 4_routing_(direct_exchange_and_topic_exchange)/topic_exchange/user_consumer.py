import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties
from pika.frame import Method


def on_message_received(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    print(f"Users Service - received new message: {body}")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='topic_exchange', exchange_type=ExchangeType.topic)

queue: Method = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='topic_exchange', queue=queue.method.queue, routing_key='user.#')

channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print('Starting Consuming')
channel.start_consuming()
