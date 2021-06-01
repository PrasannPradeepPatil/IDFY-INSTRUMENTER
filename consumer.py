#!/usr/bin/env python
import pika
import sys



connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='idfy-instrumenter', exchange_type='topic', durable=True)

result = channel.queue_declare('logstash-big-query', durable=True)
queue_name = result.method.queue

binding_keys = ["#"]
# if not binding_keys:
#     sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
#     sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='idfy-instrumenter', queue='logstash-big-query', routing_key=binding_key)




def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue='logstash-big-query', on_message_callback=callback, auto_ack=True)

channel.start_consuming()