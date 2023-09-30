from multiprocessing import Process
from publisher import temp_publisher, humid_publisher
from subscriber import sensor123_subscriber, temp_subscriber
from time import sleep

# Make sure that a RabbitMQ server is running, or otherwise
# this program will fail (see README)

# HOW:
# sudo apt-get install rabbitmq-server
# sudo service rabbitmq-server start
# sudo service rabbitmq-server stop

if __name__ == "__main__":
	p1 = Process(target=temp_publisher, args=('1',))
	p2 = Process(target=humid_publisher, args=('2',))

	c1 = Process(target=temp_subscriber, args=('temp',))
	c2 = Process(target=sensor123_subscriber, args=('sensor',))

	p1.start()
	sleep(5)
	p2.start()
	
	c1.start()
	sleep(5)
	c2.start()
	
	sleep(30) 
	c1.terminate()
	sleep(5)
	c2.terminate()

	p1.terminate()
	p2.terminate()
