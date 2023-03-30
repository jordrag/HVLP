# encoding: utf-8

""" HVLP session logic. """

from __future__ import print_function
from __future__ import unicode_literals

import logging
import logging.config
import socket
import threading

from components.packets import *
from components.errors import *


class HVLPSession(object):
    """
    Session rules for HVLP protocol.

    Attributes:
        packet: list
            Deserialized data packet.
        data: str
            Data part of the packet.
        rcvd_data: bytearray
            Received stream on connection.
        connection:
            The established connection with the client.
        addr_info: list
            Contents TCP/IP address and port info.
        broker: object
            Used broker object.
        max_size_packet: int
            Maximum packet size in bytes permitted to transmit.
        stop_event:
            A flag to close the session.

    """

    def __init__(self, connection, addr_info, broker):

        self.packet = None
        self.data = ""
        self.rcvd_data = bytearray
        self.connection = connection
        self.addr_info = addr_info
        self.broker = broker
        self.max_size_packet = 1024
        self.stop_event = threading.Event()

        logging.config.fileConfig(b"components\\hvlp_logging.conf")
        self.logger = logging.getLogger()

    def run(self, *args):
        """ Supports session between a client and the broker. """

        try:
            self.logger.info('Connection from IP: {0} and port: {1}'.format(self.addr_info[0], self.addr_info[1]))

            while True:

                # Received data through the socket
                self.rcvd_data = bytearray(self.connection.recv(self.max_size_packet))

                # Result of checked data ID and corresponding action
                broker_message = self.on_stream(self.rcvd_data)

                # Print result of checked data ID and corresponding action
                self.logger.info(broker_message)

                # Checker for "stop" flag, closing the session
                if self.stop_event.is_set():
                    self.send_reply(self.connection, broker_message)
                    break

                self.send_reply(self.connection, broker_message)

            self.logger.info('Connection from {0} closed !'.format(self.addr_info))
            self.connection.close()

        # except NotConnectedError:
        #     msg = "The client is not connected, please connect first !"
        #     self.logger.info(msg)

        except socket.error:
            self.reset_socket()

        except WrongPacket:
            msg = "Wrong packet received from: {0} ".format(self.addr_info)
            self.logger.info(msg)

        except HVLPErrors:
            self.logger.info("Illegal command received !")
            print("Illegal command received !")

    def reset_socket(self):
        """ Removes the force closed connections from broker's data. """

        topic_list = deque(self.broker.subscription)
        try:
            for topic in topic_list:
                self.broker.subscription[topic].remove(self.connection)

            self.broker.connected_clients.remove(self.connection)

        except ValueError:
            pass

        except KeyError:
            pass

        msg = "Connection {0} was force closed at the client's site ! " \
              "Data cleaned up from server. ".format(self.addr_info)

        self.logger.info(msg)

    def send_reply(self, client, broker_message):
        """ Sends short status message back to the client. """

        message_to_client = BrokerMessage(broker_message, self.data).serialize()
        client.sendall(message_to_client)

    def on_stream(self, data):
        """
        Analyzes data in the packet and depending on command ID manage what to be done in
        the broker.
        """
        try:
            self.packet = Packet.deserialize(data)

            command = self.packet.operation_id

            commands = {1: self.on_connect,
                        2: self.on_disconnect,
                        3: self.on_subscribe,
                        4: self.on_unsubscribe,
                        5: self.on_publish
                        }

            result = commands[command]()

        except (KeyError, IndexError):
            raise WrongPacket

        return result

    def on_connect(self):
        """ Connects HVLP client to the broker. """

        self.data = ""
        if self.connection not in self.broker.connected_clients:
            self.broker.connected_clients.append(self.connection)
            message = "Client {0} connected to broker !".format(self.addr_info)
        else:
            message = "Client already connected to broker !".format(self.addr_info)

        return message

    def on_disconnect(self):
        """ Disconnects HVLP client from the broker. """

        try:
            self.data = ""
            self.broker.connected_clients.remove(self.connection)
            subscription_values = self.broker.subscription.values()
            for ip_lists in subscription_values:
                if self.connection in ip_lists:
                    ip_lists.remove(self.connection)

            message = "Client {0} disconnected from broker !".format(self.addr_info)
            self.stop_event.set()

            return message

        except ValueError:
            message = "The client is not connected, no need  to disconnect !"
            return message

        except HVLPErrors:
            message = "The client is not connected, please connect first !"
            return message

    def on_subscribe(self):
        """ Checks if the client is connected to the broker and subscribe it for the desired topic. """

        self.data = ""
        topics = self.packet.topics
        topic_list = deque(topics)
        message = ""

        try:
            # Check if the client is connected
            self.broker.connected_clients.index(self.connection)

            # Take all topics defined for subscription
            subscription_keys = self.broker.subscription.keys()

            # Subscribing algorithm
            while topic_list:
                topic = topic_list.popleft()

                if topic not in subscription_keys:
                    self.broker.subscription[topic] = {self.connection}
                else:
                    self.broker.subscription[topic].add(self.connection)

                message = "Client {0} subscribed for topic: {1} ".format(self.addr_info,
                                                                         topics)
        except ValueError:
            message = "The client is not connected, please connect first !"

        except KeyError:
            message = "Missing topic !"

        return message

    def on_unsubscribe(self):
        """
        Checks if the client is connected to the broker and subscribed for the desired topic,
        then removes it from the topic list.
        """
        self.data = ""
        topics = self.packet.topics
        topic_list = deque(topics)

        message = ""

        try:
            # Check if the client is connected
            self.broker.connected_clients.index(self.connection)

            # Take all subscriptions
            subscription_values = self.broker.subscription.values()

            # Unsubscribing algorithm
            while topic_list:
                topic = topic_list.popleft()

                for ip_lists in subscription_values:
                    if self.connection in ip_lists:
                        self.broker.subscription[topic].remove(self.connection)
                        message = "Client {0} unsubscribed for topic: {1} ".format(self.addr_info,
                                                                                   topics)
                        break
                    else:
                        message = "Client {0} is not subscribed for topic: {1} ".format(self.addr_info,
                                                                                        topic)

        except ValueError:
            message = "The client is not connected, please connect first !"

        except KeyError:
            message = "Missing topic !"

        return message

    def on_publish(self):
        """
        Receives data from a publisher and distribute to every client subscribed for this topic
        except publisher itself.
        """
        message = ""
        topic = self.packet.topic
        self.data = self.packet.data

        try:
            # Check if the client is connected
            self.broker.connected_clients.index(self.connection)

            clients_list = self.broker.subscription[topic]

            for client in clients_list:
                if client != self.connection:
                    client.sendall(self.rcvd_data)
                    message = "Data from {0} published ! ".format(self.addr_info)

        except ValueError:
            self.data = ""
            message = "The client is not connected, please connect first !"

        except KeyError:
            self.data = ""
            message = "Missing topic !"

        return message
