# -*- coding: utf-8 -*-

import SocketServer
import json
from datetime import datetime


helpmessage = 'login <username> - log in with the given username \nlogout - log out \nmsg <message> - send message \nnames - list users in chat \nhelp - view help text' 

clients = {}
chatHistory = []

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

def checkValidLogin(username, list, socket):
    if socket in list:
        return False, 'Already logged in.'
    elif username == None or not(username.isalnum()):
        return False, 'Not a valid username, use only letters a-z and digits 0-9.'
    elif username in list.values():
        return False, 'Username taken.'
    else:
        return True, 'All good.'
        
            
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
        global chatHistory
        global clients

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            recieved_dict = json.loads(received_string)
            case = (recieved_dict['request']) 
            if case == 'login':
                valid, error = checkValidLogin(recieved_dict['content'], clients, self.connection)
                if valid:
                    clients[self.connection] = recieved_dict['content']
                    broadcast('login', recieved_dict['content'] + " connected", self.connection)
                    send('history', chatHistory, self.connection)
                else:
                    send('login', error, self.connection)
            elif case == 'logout':
                if self.connection in clients:
                    broadcast('logout', clients[self.connection] + " disconnected", self.connection)
                    clients.pop(self.connection, None)
                else:
                    send('error','Error: Not a valid request.', self.connection)
            elif case == 'help':
                send('help', helpmessage, self.connection)
            elif case == 'names':
                if self.connection in clients:
                    message = "Connected users: "
                    message += ", ".join(clients.values());
                    send('info', message, self.connection)
                else:
                    send('error','Error: Not a valid request.', self.connection)
            elif case == 'msg':
                if self.connection in clients:
                    broadcast('message', recieved_dict['content'], self.connection)
                else:
                    send('error','Error: Not a valid request.', self.connection)
            else:
                send('error','Error: Not a valid request.', self.connection)
                
                           
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True
    
def broadcast(response, content, selfconnection):
    global chatHistory
    dict = {'timestamp':datetime.now().strftime("%X"), 'sender':clients[selfconnection], 'response':response, 'content':content}
    
    message = json.dumps(dict)
    if response == 'message':
        chatHistory.append(dict)
    for socket in clients:
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
