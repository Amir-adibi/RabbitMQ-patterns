import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

message = 'broadcast message: Hello World!'
channel.basic_publish(exchange='pubsub', routing_key='', body=message)

print(f"sent message {message}")

connection.close()


