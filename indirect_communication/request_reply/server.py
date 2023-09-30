import zmq
from constants import *
import string

def server():
  context = zmq.Context()
  socket  = context.socket(zmq.REP)       # create reply socket
  socket.bind(f"tcp://*:{PORT_S}")        # bind socket to address

  while True:
    message = socket.recv()               # wait for incoming message
    if not b"STOP" in message:            # if not to stop...
      print(f"received: {message}")
      reply = message.decode()+'!'        # append "!" to message
      socket.send(reply.encode())         # send it away (encoded)
    else:                         
      break                               # break out of loop and end

if __name__ == "__main__":
  server()