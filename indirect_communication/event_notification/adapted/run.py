from multiprocessing import Process
from constants import *
from subscriber import client
from publisher import server

import time

if __name__ == "__main__":
  s  = Process(target=server)
  c1 = Process(target=client, args=(HUMIDTOPIC,1))
  c2 = Process(target=client, args=(TEMPTOPIC,2))

  s.start()
  c1.start()
  c2.start()
  
  time.sleep(15)
  c1.terminate()
  c2.terminate()
  s.terminate()
