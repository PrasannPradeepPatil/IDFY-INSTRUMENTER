#!/usr/bin/env python
import pika
import sys
import json
from pika import connection



def singleton(class_):
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
        self.connectRMQ()


    def connectRMQ(self):
        try:
        
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='idfy-instrumenter', exchange_type='topic',durable=True)
        except Exception as e:
            print("Connection Failed due to: ", e)


    
    
    def publishMessage(self,messageMap,routingKey):    
        if not self.connection or self.connection.is_closed:
            self.connectRMQ()
        
        messageMap  = json.dumps(messageMap).encode('utf-8')                                              
        self.channel.basic_publish(exchange='idfy-instrumenter', routing_key=routingKey, body=messageMap)
        print(" [x] Sent %r:%r" % (routingKey, messageMap))


    
    
        # connection.close()

    


   

    





