
import zmq
import time
import json
import random
from constants import *
from multiprocessing import Process

# LET OP: STUURT NIET NAAR ALLE CLIENTS, ONDANKS MEERDERE CLIENTS GEONNECTEERT NAAR PRODUCER!!! 
# ENKEL 1 op ROUND ROBIN FASHION. 
# PRODUCER WACHT DAN EEN BEETJE, EN STUURT NOGMAALS NAAR VOLGENDE CLIENT. 
# HOE WEET PRODUCER DAT CLIENT VRIJ IS? PRODUCER WACHT NIET!
# ER IS EEN QUEUE BIJ ELKE CONSUMER, EN PRODUCER DISTRIBUEERT DE TAKEN VOLGENS RR. 
# DUS ANDERS DAN WAT ER IN DE SLIDES STAAN ? SLIDES ZEGT, PRODUCER WACHT TOT ZE VRIJ ZIJN.

NWORKERS = 2
NPRODUCERS = 1

def consumer(pid):
  context = zmq.Context()
  s = context.socket(zmq.PULL)       # create a pull socket
  for producer_id in range(1, NPRODUCERS + 1):
    s.connect(f"tcp://{HOST_S}:{int(PORT_S) + producer_id}")

  while True:
    print(f"consumer {pid}: waiting for orders")
    order = json.loads(s.recv().decode())  # receive msg from any task source
    print(f"consumer {pid}: received order {order}")
    time.sleep(order["total_value"])

def producer(pid):
    context = zmq.Context()              
    socket  = context.socket(zmq.PUSH)      # create a push socket
    socket.bind(f"tcp://{HOST_S}:{int(PORT_S) + pid}")   # bind socket to address
    
    time.sleep(2)
    for i in range(10):                     # generate 10 orders
      order = json.dumps({
        'src': int(PORT_S) + pid,
        'order_id': i,
        'total_value': random.randint(0,50)
	    })
      print(f"producer  {pid} : submitting order '{order}'")
      socket.send(order.encode()) 
      time.sleep(5)

if __name__ == "__main__":
    producers = [Process(target=producer, args=(i+1,)) for i in range(NPRODUCERS)]
    consumers = [Process(target=consumer,args=(i+1,)) for i in range(NWORKERS)]

    for cons in consumers:
      cons.start()
    for prod in producers:
      prod.start()

    time.sleep(250)

    for cons in consumers:
      cons.terminate()
    for prod in producers:
      prod.terminate()