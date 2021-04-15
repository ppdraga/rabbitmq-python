import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=25672))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message,
    # properties=pika.BasicProperties(
    #     delivery_mode=2,  # make message persistent
    # )
)
print(" [x] Sent %r" % message)
connection.close()
