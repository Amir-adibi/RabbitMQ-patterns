import pika

def on_message_received(ch, method, properties, body):
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
