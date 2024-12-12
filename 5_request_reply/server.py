import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


def on_request_message_received(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    print(f'request received: {properties.correlation_id}')
    ch.basic_publish('', routing_key=properties.reply_to, body=f'Hey, its your reply to {properties.correlation_id}')


connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='request_queue')

channel.basic_consume(queue='request_queue', auto_ack=True, on_message_callback=on_request_message_received)

print('Starting Server')

channel.start_consuming()
