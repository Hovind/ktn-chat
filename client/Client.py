# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        # TODO: Our stuff
        receiver = MessageReceiver(self, self.connection)
            
        # Read input from user
        while (True):
            input = raw_input('Skriv noe: ')
            input = input.split(' ', 1)
            payload = {'request': input[0], 'content': input[1]}
            send_payload(payload)

        
    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        parser = MessageParser(message)

    def send_payload(self, data):
        # TODO: Handle sending of a payload
		payload_string = json.dumps(data)
		self.connection.send(payload_string)
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
