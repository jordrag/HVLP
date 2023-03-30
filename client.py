""" HVLP client """

# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import sys
import socket
import threading
from time import *

from components.packets import *
from client_menu import MenuHVLP as menu
import components.errors as error

sys.path.append(str("."))
sys.path.append(str(".."))


class Client(object):
    """
    Implementation of client for establishing connections to broker type server.
    Attributes:
        srv_addr: str
            The TCP address of HVLP broker.
        port: int
            The IP port of HVLP broker.

    """

    def __init__(self, srv_addr, port):
        self.srv_addr = srv_addr
        self.port = port
        self.sock = socket.socket()
        self.lock = threading.Lock()
        self.rcvd_data = None
        self.sent_data = None
        self.disconnect_flag = False
        self.stop_event = threading.Event()
        self.receive_part = None

    def send_packet(self, message):
        """ Sends data to broker. """

        try:
            with self.lock:
                self.sent_data = message
                self.sock.sendall(message)
                if self.disconnect_flag:
                    self.disconnect_flag = False
                    self.close_sock()

        except socket.error:
            raise error.NotConnectedError

    def receive_packet(self):
        """ Receives data from broker. """

        self.lock_print("Receiving started ... ")
        # self.rcvd_data = ""

        while not self.stop_event.is_set():
            # Receives data back from the broker and deserializes it

            try:
                self.rcvd_data = self.sock.recv(1024)
                data = Packet.deserialize(self.rcvd_data)

                if data.operation_id == 99 or data.operation_id == 5:

                    # Check the trigger for stopping message. If there is one - stops the client.
                    data_checker = self.manage_data(data)

                    self.lock_print(data_checker)

                    if "Stop" in data_checker:
                        break

            except socket.error:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()

            except AttributeError:
                self.rcvd_data = ""

            except WrongPacket:
                pass

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    @staticmethod
    def manage_data(data):
        """
        Analyzes data in the packet and depending on command ID manage what to be done in
        the client.
        """
        message = ""

        if data.operation_id == 99:
            message = ("""\n
            Server info: {}
            
            """).format(data.message)
            if "disconnected" in data.message:
                message = "Stop, client disconnected from server !"

        elif data.operation_id == 5:
            message = ("""\n
            Server info: topic -> {0}, data -> {1}

            """).format(data.topic, data.data)

        return message

    # @staticmethod
    def connect(self):
        """ Returns connect message template. """

        try:
            self.disconnect_flag = False
            self.sock.connect((self.srv_addr, self.port))
            mes = ("\nSetup client at: {0} and port {1}".format(self.srv_addr, self.port))
            self.lock_print(mes)

        except socket.error:
            mes = "Server is not accessible !"
            self.lock_print(mes)

        self.receive_part = threading.Thread(target=self.receive_packet)
        self.receive_part.start()

        result = Connect(payload="").serialize()

        return result

    def disconnect(self):
        """ Returns disconnect message template. """

        result = Disconnect(payload="").serialize()
        self.disconnect_flag = True
        self.stop_event.set()

        return result

    @staticmethod
    def subscribe(topics_list):
        """ Takes all user's topics and packet them in a topic list. """

        result = Subscribe(topics_list).serialize()
        return result

    @staticmethod
    def unsubscribe(topics_list):
        """ Takes all user's topics and packet them in a topic list. """

        result = Unsubscribe(topics_list).serialize()
        return result

    @staticmethod
    def publish(topic, data):
        """ Takes topic and raw data from the user. """

        result = Publish(topic, data).serialize()
        return result

    def lock_print(self, *args, **kwargs):
        """ Locks console for printing."""

        self.lock.acquire()
        print(*args, **kwargs)
        self.lock.release()

    def close_sock(self):
        """ Closes socket immediately after disconnect. """

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b'\1\0\0\0\0\0\0\0')
        self.sock.close()


# ******************** Data for some connections ***************************

client = Client(srv_addr='172.20.10.45', port=65432)

# **************************************************************************

# Starts a client with defined data

if __name__ == "__main__":
    menu(client).choice()
