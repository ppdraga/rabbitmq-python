import time
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 25672))
    channel = connection.channel()
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare(queue='', exclusive=True) # random named queue
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    print('binding_keys', binding_keys)
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_keys]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

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
