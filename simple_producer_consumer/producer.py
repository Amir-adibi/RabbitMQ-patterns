import pika

connection_parameters = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='testName')

message = 'Hello World!'
channel.basic_publish(exchange='', routing_key='testName', body=message)

print(f"sent message {message}")

connection.close()


