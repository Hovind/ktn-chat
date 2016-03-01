from socket import *
import cPickle as pickle
from datetime import datetime


class Messages:
	username = ''
	message = ''
	timestamp = ''
	address = ''
	def __init__(self, username):
		self.username = username
	def new_message(self, new_message):
		self.message = new_message
	def set_timestamp(self):
		self.timestamp = datetime.now().strftime("%X")

		
		
client = Messages(raw_input('Your username: '));


s = socket(AF_INET, SOCK_STREAM)
PORT = 40000
s.connect(('127.0.0.1', PORT))
while(1):
	client.message = raw_input('Your message: ')
	client.set_timestamp()
	#pickle_out = open("message_object.pickle", "wb")
	data_string = pickle.dumps(client, -1)
	s.send(data_string)
	#pickle_out.close()
	print 'Awaiting reply'
	reply = s.recv(1024)
	print "Recieved: ", repr(reply)
	
s.close()