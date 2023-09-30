from multiprocessing import Process
import zmq
import random
import time
import json
from constants import *

def server():
  context = zmq.Context()         
  socket = context.socket(zmq.PUB)          # create a publisher socket
  socket.bind(f"tcp://*:{PORT_S}")          # bind socket to the address

  time.sleep(5)
  i = 0
  while True:
    temp_data = json.dumps({                     # create JSON object with some fake sensor data
      'seq': i,
      'id': 'sensor123',
      'temp': random.randint(0,50),
    })
    humid_data = json.dumps({                     # create JSON object with some fake sensor data
      'seq': i,
      'id': 'sensor124',
      'humidity': random.randint(0,100),
    })

    message = TEMPTOPIC + temp_data                 # prefix with 'topic' on which subscribers can match
    socket.send(message.encode())                 # publish the temp message
    print(f"server: emit event: '{message}'")

    message = HUMIDTOPIC + humid_data            # prefix with 'topic' on which subscribers can match
    socket.send(message.encode())                 # publish the humid message
    print(f"server: emit event: '{message}'")

    i += 1
    time.sleep(5)

if __name__ == "__main__":
  server()