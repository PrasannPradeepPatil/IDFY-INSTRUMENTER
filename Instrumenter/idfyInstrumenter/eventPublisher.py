#!/usr/bin/env python
import pika
import sys
import json
from pika import connection

'''
1.SELECTION CONNECTION 
https://stackoverflow.com/questions/30332320/how-to-do-a-simple-pika-selectconnection-to-send-a-message-in-python


2.BLOACKING CONNECTTION
https://pika.readthedocs.io/en/stable/examples/heartbeat_and_blocked_timeouts.html
https://stackoverflow.com/questions/46053349/keep-pika-blockingconnection-alive-without-disabling-heartbeat
https://stackoverflow.com/questions/56322608/allow-rabbitmq-and-pika-maintain-the-conection-always-open

sudo docker run --rm -it --name my-rabbit --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

'''

def singleton(class_):
    # https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


# @singleton
class PublishMessage:
    __instance = None
    @staticmethod 
    def getInstance():
      """ Static access method. """
      if PublishMessage.__instance == None:
         PublishMessage()
      return PublishMessage.__instance


    def __init__(self):   
        """ Virtually private constructor. """
        if PublishMessage.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            PublishMessage.__instance = self
   
        self.connection = None
        self.channel = None
        self.connect_RMQ()


    def connect_RMQ(self):
        try:
        
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='idfy-instrumenter', exchange_type='topic',durable=True)
        except Exception as e:
            print("Connection Failed due to: ", e)

    # def reconnect_RMQ(self):
    #     print("RECONNECTING TO RMQ......")
    #     self.connect_RMQ(callback=None)
  
 
    
    
    def publish_message(self,message_map,routing_key):    
        if not self.connection or self.connection.is_closed:
            self.connect_RMQ()
        
        message_map  = json.dumps(message_map).encode('utf-8')                                              
        self.channel.basic_publish(exchange='idfy-instrumenter', routing_key=routing_key, body=message_map)
        print(" [x] Sent %r:%r" % (routing_key, message_map))


    
    
        # connection.close()

    


   

    





