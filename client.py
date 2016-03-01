from socket import *
#import cPickle as pickle
from datetime import datetime
import json

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

		
		
#client = Messages(raw_input('Your username: '));

dict = {'request':'help','content':'None'}
s = socket(AF_INET, SOCK_STREAM)
PORT = 40000
s.connect(('127.0.0.1', PORT))
while(1):
	message = raw_input('Your message: ')
	#client.set_timestamp()
	#pickle_out = open("message_object.pickle", "wb")
	data_string = json.dumps(dict)
	s.send(data_string)
	#pickle_out.close()
	print 'Awaiting reply'
	reply = s.recv(4096)
	#print reply
	a = json.loads(reply)
	print repr(a)
	
s.close()