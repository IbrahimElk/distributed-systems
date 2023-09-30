import rabbitpy
import time
import random
import json
from constants import *

# INFO: 

# ----------------------- CHANNELS ---------------------------------
# Some applications need multiple logical connections to the broker. 
# However, it is undesirable to keep many TCP connections open at the same 
# time because doing so consumes system resources and makes it more difficult to configure firewalls.

# AMQP connections are multiplexed with channels that can be thought of as 
# "lightweight connections that share a single TCP connection".
# For applications that use multiple threads/processes for processing, it is very common to open 
# a new channel per thread/process and not share channels between them.

# ----------------------- EXCHANGES ---------------------------------
# Messages are published to exchanges, which are often compared to post offices or mailboxes.
# Exchanges then distribute message copies to queues. 
# Then the broker either deliver messages to consumers subscribed to queues, 
# or consumers fetch/pull messages from queues on demand.

# The routing algorithm used depends on the exchange type. 
# Topic exchanges route messages to one or many queues based on matching between 
# a message routing key and the pattern that was used to bind a queue to an exchange.


#--------------------------------------------------------------------------------------
# multiple clients, 1 producer, 1 exchange: 
# create a new queue from the new consumer thread, 
# have it connect to the exchange object (for which you should have a name), 
# and let the producer thread send its messages to the exchange object exclusively. 
# Any new thread may follow the same protocol.

# Each channel is a separate process within Rabbit, and it's the
# channel that does the routing logic, before passing the message to any
# destination queues. Thus all channels can route through the same
# exchanges in parallel.



def temp_publisher(id):
  connection = rabbitpy.Connection(BROKER_URL) # Connect to RabbitMQ server
  channel = connection.channel()     # Create new channel on the connection

  # Create a "topic" exchange to post sensor data
  exchange = rabbitpy.Exchange(channel, EXCHANGE_ID, exchange_type='topic')
  exchange.declare() # ensure exchange exists on the server
  # can remove using exchange.delete()

  time.sleep(5)
  for i in range(25):
    data = {'seq': i, 'id': 'sensor123', 'temp': random.randint(0,50)}
    message = rabbitpy.Message(channel, json.dumps(data)) # serialize data to string
    print(f"publisher {id} : emitting event '{data}'")
    # Publish the message using a "routing key"
    message.publish(exchange, 'temp.sensor123')

    time.sleep(10)

    data = {'seq': i, 'id': 'sensor124', 'temp': random.randint(0,50)}
    message = rabbitpy.Message(channel, json.dumps(data)) # serialize data to string
    print(f"publisher {id} : emitting event '{data}'")
    # Publish the message using a "routing key"
    message.publish(exchange, 'temp.sensor124')
    time.sleep(10)

def humid_publisher(id):
  connection = rabbitpy.Connection(BROKER_URL) 
  channel = connection.channel()     

  exchange = rabbitpy.Exchange(channel, EXCHANGE_ID, exchange_type='topic')
  exchange.declare() 

  time.sleep(5)
  for i in range(25):
    data = {'seq': i, 'id': 'sensor124', 'humid': random.randint(0,10)}
    message = rabbitpy.Message(channel, json.dumps(data)) 
    print(f"publisher {id} : emitting event '{data}'")
    message.publish(exchange, 'humid.sensor124')
  
    time.sleep(10)

    data = {'seq': i, 'id': 'sensor124', 'humid': random.randint(0,10)}
    message = rabbitpy.Message(channel, json.dumps(data)) 
    print(f"publisher {id} : emitting event '{data}'")
    message.publish(exchange, 'humid.sensor124')

    time.sleep(10)

if __name__ == "__main__":
  temp_publisher(1)
  humid_publisher(2)