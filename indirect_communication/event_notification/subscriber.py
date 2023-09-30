import zmq
import json
import random
from constants import *

def client(topic:str, clientid:int):
  context = zmq.Context()
  socket = context.socket(zmq.SUB)                  # create a subscriber socket
  socket.connect(f"tcp://{HOST_S}:{PORT_S}")        # connect to the server
  socket.setsockopt(zmq.SUBSCRIBE, topic.encode())  # subscribe to TEMP messages (filter on prefix)
  
  # WHY do i need to set the topic here as option, if i will still manually lstrip the desired prefix? 
  # Because, you dont receive the other messages with other prefixes. 

  while True:
    msg = socket.recv()                      # receive a message related to subscription
    data = str(msg.decode()).lstrip(topic)   # strip the TEMP prefix
    data = json.loads(data)                  # parse the JSON object
    print(f"client {clientid} : received event: {data}")    
    if (topic == TEMPTOPIC and data['temp'] > 30):
      print(f"warning: high temperature measured by sensor {data['id']}")


if __name__ == "__main__":
  coinflip = random.randint(0,1)
  if(coinflip == 0):
    client(TEMPTOPIC,1)
  else:
    client(HUMIDTOPIC,1)
