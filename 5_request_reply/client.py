import pika
from pika.frame import Method
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import uuid

def on_reply_message_received(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    print(f'reply received: {body}')

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

reply_queue: Method = channel.queue_declare(queue='', exclusive=True)
channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True, on_message_callback=on_reply_message_received)

channel.queue_declare(queue='reqeust_queue')
message = 'Can I reqeust a reply?'
correlation_id = str(uuid.uuid4())

print(f'Sending request: {correlation_id}')

channel.basic_publish(
    exchange='',
    routing_key='request_queue',
    properties=pika.BasicProperties(
        reply_to=reply_queue.method.queue,
        correlation_id=correlation_id
    ),
    body=message
)

print('Starting Client')

channel.start_consuming()
