# -*- coding: utf-8 -*-

import SocketServer
import json
from datetime import datetime


helpmessage = 'login <username> - log in with the given username \n logout - log out \n msg <message> - send message \n names - list users in chat \n help - view help text' 

clients = {}

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        
        

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            recieved_dict = json.loads(received_string)
            case = (recieved_dict['request']) 
            if case == 'login':
                clients[self.connection] = recieved_dict['content']
                broadcast('login', recieved_dict['content'] + " connected")
            elif case == 'logout':
                if self.connection in clients:
                    broadcast('logout', recieved_dict['content'] + "disconnected")
                    clients.pop(self.connection, None)
                else:
                    send('logout','Error: Not a valid request.', self.connection)
            elif case == 'help':
                send('help', helpmessage, self.connection)
            elif case == 'names':
                if self.connection in clients:
                    message = "Connected users: "
                    for key in clients:
                        message += clients[key] + ", "
                    send('names', 'message', self.connection)
                else:
                    send('names','Error: Not a valid request.', self.connection)
            elif case == 'msg':
                if self.connection in clients:
                    broadcast('msg', recieved_dict['content'])
                else:
                    send('msg','Error: Not a valid request.', self.connection)
            else:
                send('error','Error: Not a valid request.', self.connection)
                
                
            
        
            
            
            
            
            # TODO: Add handling of received payload from client

            
            
            
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True
    
def broadcast(response, content):
    for socket in clients:
        dict = {'timestamp':datetime.now().strftime("%X"), 'sender':clients[socket], 'response':response, 'content':content}
        message = json.dumps(dict)
        try :
            socket.send(message)
        except :
            # broken socket connection
            socket.close()
            # broken socket, remove it
            if socket in clients:
                clients.pop(socket, None)

				
def send(response, content, socket):
    dict = {'timestamp':datetime.now().strftime("%X"), 'sender':None, 'response':response, 'content':content}
    message = json.dumps(dict)
    try :
        socket.send(message)
    except :
        # broken socket connection
        socket.close()
        # broken socket, remove it
        #if socket in clients:
        #    clients.pop(socket, None)

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = '127.0.0.1', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
