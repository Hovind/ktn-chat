from socket import *
from threading import Thread
import cPickle as pickle
from datetime import datetime

class Messages:
	username = ''
	message = ''
	timestamp = ''
	def __init__(self, username):
		self.username = username
	def new_message(self, new_message):
		self.message = new_message
	def set_timestamp(self):
		self.timestamp = datetime.now().strftime("%X")


Client_adresses = []

def clientHandler():
	conn, addr = s.accept()
	global Client_adresses
	Client_adresses.append(addr)
	print addr, "is connected"
	while(1):
		data = conn.recv(1024)
		data_loaded = pickle.loads(data)
		#data_loaded.address = addr
		if data:
			print data_loaded.timestamp, " - ", data_loaded.username, "sent:", repr(data_loaded.message)
			# for i in range(len(Client_adresses)):
				# message = addr, "said: ", repr(data)
				# if addr != Client_adresses[i]:
					# s.sendto(data, ('<broadcast>', PORT))
		else: break	


HOST = '127.0.0.1' #Local host
PORT = 40000
num_of_clients = 3

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(num_of_clients)

print "Server is running......"

for i in range(num_of_clients):
	Thread(target=clientHandler).start()

s.close()


# while(1):
	# data = conn.recv(1024)
	# print "Recieved: ", repr(data)
	# reply = raw_input("Reply: ")
	# conn.sendall(reply)
	
# conn.close()
