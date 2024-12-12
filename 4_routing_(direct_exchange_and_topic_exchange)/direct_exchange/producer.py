import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

message = 'This message needs to be routed'
channel.basic_publish(exchange='routing', routing_key='analytics_only', body=message)

message = 'Broadcast message'
channel.basic_publish(exchange='routing', routing_key='both', body=message)

print(f"sent message {message}")

connection.close()


