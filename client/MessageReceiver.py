# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):

    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        super(MessageReceiver, self).__init__()
        # Flag to run thread as a daemon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.connection = connection
        self.start()

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while(True):
            response = self.connection.recv(1024)
            self.client.receive_message(response)

    def receive(self):
        pass
