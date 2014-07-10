import pika
import logging
import json
import sys

logging.getLogger('pika').setLevel(logging.DEBUG)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

message = { 'cmd':'prv',
            'id':sys.argv[1]
           }

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=json.dumps(message))
print " [x] Sent 'Hello World!'"
connection.close()