import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from pika.exchange_type import ExchangeType
from pika.frame import Method


def on_message_received(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    print(f"first_consumer received new message: {body}")


connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
# The exchange declared both in producer end and the consumer end
# It is because if the consumer starts its job before the producer, the exchange exists and the program does not encounter with any error
channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# If the name of the queue is an empty string, the rabbitMQ itself chooses a random name
# The exclusive flag determines the queue is dedicated to this consumer. once the consumer's connection is closed, the queue will be deleted.
queue: Method = channel.queue_declare(queue='', exclusive=True)

# once the queue is declared, the queue should be bind to the exchange
channel.queue_bind(exchange='pubsub', queue=queue.method.queue)

channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print('Starting Consuming')
channel.start_consuming()
