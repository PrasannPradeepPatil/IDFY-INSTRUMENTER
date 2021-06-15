#!/usr/bin/env python
import pika
import sys
import json
import logging
from pika import connection



class Publisher:
    __instance = None
    @staticmethod 
    def getInstance():
      """ Static access method. """
      if Publisher.__instance == None:
         Publisher()
      return Publisher.__instance


    def __init__(self):   
        """ Virtually private constructor. """
        if Publisher.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Publisher.__instance = self
   
        self.connection = None
        self.channel = None
        self.connect_rmq()


    def connect_rmq(self):
        try:
        
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='idfy-instrumenter', exchange_type='topic',durable=True)
        except Exception as e:
            logging.error("Connection Failed due to: ", e)


 
    
    def publish_message(self,messageMap,routingKey):    
        if not self.connection or self.connection.is_closed:
            self.connect_rmq()
        
        messageMap  = json.dumps(messageMap).encode('utf-8')                                              
        self.channel.basic_publish(exchange='idfy-instrumenter', routing_key=routingKey, body=messageMap)
        # print(" [x] Sent %r:%r" % (routingKey, messageMap))


    
    
        # connection.close()

    


   

    





