import pika
import time
import random
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

def on_message_received(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    processing_time = random.randint(1, 6)
    print(f"received : {body}, will take {processing_time} to process")
    time.sleep(processing_time)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('Finished processing the message')


connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.queue_declare(queue='testName')

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue='testName',
    on_message_callback=on_message_received
)


print('Starting Consuming')
channel.start_consuming()