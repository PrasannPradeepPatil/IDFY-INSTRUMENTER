#!/usr/bin/env python
import pika
import sys
import json


def publish_message(message_map, routing_key):
    # CREATE CONNECTION TO RABBITMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()


    #PUBLISH TO RABBITMQ
    channel.exchange_declare(exchange='idfy-instrumenter', exchange_type='topic',durable=True)

 
    
    # message = Jason.encode!(message_map) 
    message_map  = json.dumps(message_map).encode('utf-8')                                              
    
    channel.basic_publish(exchange='idfy-instrumenter', routing_key=routing_key, body=message_map)

    print(" [x] Sent %r:%r" % (routing_key, message_map))


    connection.close()


