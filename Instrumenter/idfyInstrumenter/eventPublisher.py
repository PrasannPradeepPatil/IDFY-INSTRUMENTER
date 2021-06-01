#!/usr/bin/env python
import pika
import sys
import json


class PublishMessage:
    def __init__(self):
        # CREATE CONNECTION TO RABBITMQ-->https://stackoverflow.com/questions/30332320/how-to-do-a-simple-pika-selectconnection-to-send-a-message-in-python
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # connection =  pika.SelectConnection(pika.ConnectionParameters(heartbeat=600,host='localhost'))
        self.channel = connection.channel()


        #PUBLISH TO RABBITMQ
        self.channel.exchange_declare(exchange='idfy-instrumenter', exchange_type='topic',durable=True)

    
    def publish_message(self,message_map,routing_key):    
        # message = Jason.encode!(message_map) 
        message_map  = json.dumps(message_map).encode('utf-8')                                              
        
        self.channel.basic_publish(exchange='idfy-instrumenter', routing_key=routing_key, body=message_map)

        print(" [x] Sent %r:%r" % (routing_key, message_map))


    
        # connection.close()

    


    





