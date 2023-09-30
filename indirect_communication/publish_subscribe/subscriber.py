import rabbitpy
import sys
import json
from constants import *

# THIS IS A CASE WHERE SUBSCRIBERS POLL THEIR QUEUE, see command ``for message in queue``
# THEY DONT RECEIVE A PUSH NOTIFCATION FROM THE BROKER. 

def temp_subscriber(id):
  connection = rabbitpy.Connection(BROKER_URL)
  channel =  connection.channel()

  queue = rabbitpy.Queue(channel, f'subscriber-{id}')
  queue.declare() # ensure queue exists on the server
  queue.bind(EXCHANGE_ID, 'temp.*') # Bind queue to exchange via routing key

  print(f"subscriber {id}: connected to queue")

  try:
      # Consume messages in queue (blocking if none are available)
      for message in queue:
        data = json.loads(message.body.decode())
        print(f"subscriber {id}: got message {data}")
        if (data['temp'] > 30):
            print(f"warning: high temperature measured by sensor {data['id']}")
        # explicitly acknowledge message receipt after successful processing
        message.ack()

  # Exit on CTRL-C
  except KeyboardInterrupt:
      print(f'subscriber {id}: stopped')



def sensor123_subscriber(id):
  connection = rabbitpy.Connection(BROKER_URL)
  channel =  connection.channel()

  queue = rabbitpy.Queue(channel, f'subscriber-{id}')
  queue.declare()
  queue.bind(EXCHANGE_ID, 'temp.sensor123') 
  queue.bind(EXCHANGE_ID, 'humid.sensor123') 

  print(f"subscriber {id}: connected to queue")

  try:
      for message in queue:
        data = json.loads(message.body.decode())
        print(f"subscriber {id}: got message {data}")
        message.ack()

  except KeyboardInterrupt:
      print(f'subscriber {id}: stopped')


if __name__ == "__main__":
  temp_subscriber(1)
  sensor123_subscriber(2)