# encoding: utf-8

"""
An interpretation of server(broker) which could work with any kind of session protocol.
"""

from __future__ import print_function
from __future__ import unicode_literals

import sys

import logging.config
from components.session import *

sys.path.append(str("."))


class Server(object):
    """
    Returns server session with predefined type of it. In this case it's HVLP broker.

    Attributes:
        session_type: object
            Preferred session type.
        ip_addr: str
            Client's TCP address.
        port: int
            Client's IP port.
        session_type: obj
            Preferred user's session type.
        srv_sock: socket
            Initial socket for every new connection.
        subscription: dict
            List of all defined topics and subscribed for them clients.
        connected_clients: list
            All connected clients to the broker.
    """

    def __init__(self, session_type, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port
        self.session_type = session_type
        self.srv_sock = socket.socket()
        self.subscription = {}
        self.connected_clients = []
        logging.config.fileConfig(b"components\\hvlp_logging.conf")
        self.logger = logging.getLogger()

    def run(self):
        """ Make socket connection, define separated thread for each client and starts it in
        session of any type.
        """
        try:
            self.srv_sock.bind((self.ip_addr, self.port))
            self.srv_sock.listen(5)
            self.logger.info("HVLP broker started, waiting for client's connections........")

            while True:
                # Takes info from socket established connection between Broker and Client:
                # 'connection' - contents all needed parameters
                # 'addr_info' - contents TCP address + IP port

                connection, addr_info = self.srv_sock.accept()

                # Makes a new session based on the taken above data, each session in separated thread
                session = self.session_type(connection, addr_info, self)
                session_thread = threading.Thread(target=session.run, args=[connection, addr_info])
                session_thread.start()

        except socket.error:
            self.logger.info("\nThe broker is already started ! Please check again.\n")

# Start server with defined data
if __name__ == "__main__":
    server = Server(HVLPSession, '172.20.10.45', 65432)
    # server = Server(HVLPSession, 'localhost', 65432)
    server.run()
