import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


def on_message_received(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    print(f"received new message: {body}")

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare(queue='testName')
channel.basic_consume(queue='testName', auto_ack=True, on_message_callback=on_message_received)
# message = channel.basic_get(queue='testName', auto_ack=True)
# print(message)

print('Starting Consuming')
channel.start_consuming()
