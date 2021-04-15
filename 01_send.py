import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 25672))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
connection.close()
print(" [x] Sent 'Hello World!'")

