#!/usr/bin/env python
import pika
import sys


def publish_message(message_map, routing_key):
    # CREATE CONNECTION TO RABBITMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()


    #PUBLISH TO RABBITMQ
    channel.exchange_declare(exchange='idfy-instrumenter', exchange_type='topic')

    routing_key = routing_key
    
    # message = Jason.encode!(message_map)                                                  HOW TO ENCODE IN PYTHON
    
    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)

    print(" [x] Sent %r:%r" % (routing_key, message))


    connection.close()


