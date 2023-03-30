""" An interpretation of HVLP client with user's data taken from console."""

# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import sys
import logging
import logging.config
from time import *
from client import Client


sys.path.append(str("."))
sys.path.append(str(".."))

logging.config.fileConfig(b"..\\components\\test_logging.conf")


IP_ADDR = '172.20.10.45'
# IP_ADDR = 'localhost'
# IP_ADDR = '172.20.10.80' #Ico
# IP_ADDR = '172.20.10.97' # Branko's broker
PORT = 65432


class HVLP_NET_05_01_01(object):
    """ Test for PUBLISH operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto", "moto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publish
        packet = self.sender.publish("moto", "test1")
        self.sender.send_packet(packet)
        sleep(0.1)

        # Parse sent and received data
        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result


class HVLP_NET_05_02_01(object):
    """ Test for PUBLISH operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto", "moto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publish
        packet = self.sender.publish("loto", "test1")
        self.sender.send_packet(packet)
        sleep(0.1)

        # Parse sent and received data
        if self.sender.sent_data != self.receiver.rcvd_data:
            result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result


class HVLP_NET_04_01_01(object):
    """ Test for UNSUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""

        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["moto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data()

        # Checks if received data
        parsing = self.parsing_data()
        if parsing:

            # Receiver unsubscribes
            packet = self.receiver.unsubscribe(["toto"])
            self.receiver.send_packet(packet)
            sleep(0.1)

            # Sender sends data again
            self.publish_data()

            # Checks if received data
            parse_result = self.parsing_data()
            if not parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self):
        """ Sender publish. """

        packet = self.sender.publish("toto", "test1")
        self.sender.send_packet(packet)
        sleep(0.1)


class HVLP_NET_04_01_02(object):
    """ Test for UNSUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto", "moto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data("toto")

        # Checks if received data
        parsing = self.parsing_data()

        if parsing:

            # Receiver unsubscribes
            packet = self.receiver.unsubscribe(["toto"])
            self.receiver.send_packet(packet)
            sleep(0.1)

            # Sender sends data again
            self.publish_data("moto")

            # Checks if received data
            parse_result = self.parsing_data()
            if parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self, topic):
        """ Sender publish. """

        packet = self.sender.publish(topic, "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


class HVLP_NET_04_02_01(object):
    """ Test for UNSUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["moto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data()

        # Checks if received data
        parsing = self.parsing_data()
        if parsing:

            # Sender sends data again
            self.publish_data()

            # Checks if received data
            parse_result = self.parsing_data()
            if parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self):
        """ Sender publish. """

        packet = self.sender.publish("toto", "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


class HVLP_NET_04_02_02(object):
    """ Test for UNSUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto", "moto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data("toto")

        # Checks if received data
        parsing = self.parsing_data()

        if parsing:

            # Sender sends data again
            self.publish_data("moto")

            # Checks if received data
            parse_result = self.parsing_data()
            if parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self, topic):
        """ Sender publish. """

        packet = self.sender.publish(topic, "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


class HVLP_NET_03_01_01(object):
    """ Test for SUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto", "moto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publish
        packet = self.sender.publish("moto", "test1")
        self.sender.send_packet(packet)
        sleep(0.1)

        # Parse sent and received data
        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result


class HVLP_NET_03_01_02(object):
    """ Test for SUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto", "moto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data("toto")
        sleep(0.1)

        # Checks if received data
        parsing = self.parsing_data()

        if parsing:

            # Sender sends data again
            self.publish_data("moto")

            # Checks if received data
            parse_result = self.parsing_data()
            if parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self, topic):
        """ Sender publish. """

        packet = self.sender.publish(topic, "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


class HVLP_NET_03_02_01(object):
    """ Test for SUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Sender publish
        packet = self.sender.publish("moto", "test1")
        self.sender.send_packet(packet)
        sleep(0.1)

        # Parse sent and received data
        if self.sender.sent_data != self.receiver.rcvd_data:
            result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result


class HVLP_NET_03_02_02(object):
    """ Test for SUBSCRIBE operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data("toto")
        sleep(0.1)

        # Checks if received data
        parsing = self.parsing_data()

        if not parsing:

            # Sender sends data again
            self.publish_data("moto")
            sleep(0.1)

            # Checks if received data
            parse_result = self.parsing_data()
            if not parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self, topic):
        """ Sender publish. """

        packet = self.sender.publish(topic, "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


class HVLP_NET_02_01_01(object):
    """ Test for DISCONNECT operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["moto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data()
        sleep(0.1)

        # Checks if received data
        parsing = self.parsing_data()
        if parsing:

            # Receiver disconnect
            packet = self.receiver.disconnect()
            self.receiver.send_packet(packet)

            # Sender sends data again
            self.publish_data()

            # Checks if received data
            parse_result = self.parsing_data()
            if not parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self):
        """ Sender publish. """

        packet = self.sender.publish("toto", "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


class HVLP_NET_02_02_01(object):
    """ Test for DISCONNECT operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["moto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data()

        # Checks if received data
        parsing = self.parsing_data()
        if parsing:

            # Sender sends data again
            self.publish_data()

            # Checks if received data
            parse_result = self.parsing_data()
            if parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self):
        """ Sender publish. """

        packet = self.sender.publish("toto", "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


class HVLP_NET_01_01_01(object):
    """ Test for CONNECT operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["toto", "moto", "loto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto", "moto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publish
        packet = self.sender.publish("moto", "test1")
        self.sender.send_packet(packet)
        sleep(0.1)

        # Parse sent and received data
        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        # Receiver disconnect
        packet = self.receiver.disconnect()
        self.receiver.send_packet(packet)

        return result


class HVLP_NET_01_02_01(object):
    """ Test for CONNECT operation. """

    def __init__(self):
        self.sender = Client(srv_addr=IP_ADDR, port=PORT)
        self.receiver = Client(srv_addr=IP_ADDR, port=PORT)
        self.logger = logging.getLogger()

    def execute(self):
        """ Executes test."""
        result = 0

        # Sender connects to broker
        packet = self.sender.connect()
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver connects to broker
        packet = self.receiver.connect()
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender subscribes
        packet = self.sender.subscribe(["moto"])
        self.sender.send_packet(packet)
        sleep(0.1)

        # Receiver subscribes
        packet = self.receiver.subscribe(["toto"])
        self.receiver.send_packet(packet)
        sleep(0.1)

        # Sender publishes data
        self.publish_data()
        sleep(0.1)

        # Checks if received data
        parsing = self.parsing_data()
        if parsing:

            # Receiver disconnect
            packet = self.receiver.disconnect()
            self.receiver.send_packet(packet)

            # Sender sends data again
            self.publish_data()

            # Checks if received data
            parse_result = self.parsing_data()
            if not parse_result:
                result = True
        else:
            result = False

        # Sender disconnect
        packet = self.sender.disconnect()
        self.sender.send_packet(packet)

        return result

    def parsing_data(self):
        """ Parse sent and received data """

        if self.sender.sent_data == self.receiver.rcvd_data:
            result = True
        else:
            result = False

        return result

    def publish_data(self):
        """ Sender publish. """

        packet = self.sender.publish("toto", "test1")
        self.sender.send_packet(packet)
        sleep(0.2)


if __name__ == "__main__":
    r = HVLP_NET_01_01_01().execute()
    print (r)
