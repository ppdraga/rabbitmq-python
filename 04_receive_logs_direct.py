import time
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 25672))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True) # random named queue
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for severity in severities:
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name,
                        auto_ack=True,
                        on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
