# coding=utf-8


""" Module for construction(serialization) and deconstruction(deserialization) of HVLP packets. """

from __future__ import print_function
from __future__ import unicode_literals

from collections import deque
from components.errors import *


class Packet(object):
    """
    A parent class for all commands.

    Attributes:
        packet: list
            Managed data in HVLP format packet ready for transfer.
        length: int
            The length of payload.
        payload: list
            Individual prepared payload depending on received command.
        operation_id: int
            ID of every kind of operation(command).
    Methods:
        serialize:
            Serialize and prepare for transfer HVLP packet.
            Works with predefined payload specific for each operation.
        deserialize:
            Plays like a manager for packets received for deserialization. Takes the initial part of
            the packet and depending of operation ID redirects the payload for additional work in
            the specific operation method.
    """

    def __init__(self, operation_id, payload):
        self.packet = []
        self.length = len(payload)
        self.payload = payload
        self.operation_id = operation_id

    def __str__(self):
        message = "PACKET {0} | LEN {1} | PAYLOAD {2}".format(
            self.operation_id,
            self.length,
            self.payload
        )
        return message

    def serialize(self):
        """ Serialize input data to a packet ready for transfer. """

        # Generate the length of payload
        payload_len = int(len(self.payload))

        # Generate the initial part of the packet
        self.packet = [self.operation_id, payload_len]

        # Extends the packet with payload (topic(s) + data(if presents))
        self.packet.extend(self.payload)

        return bytearray(self.packet)

    @staticmethod
    def deserialize(stream):
        """
        The manager itself.

        Args:
            stream: str
            Received on established connection packet for deserialization.
        """
        try:
            packet = bytearray(stream)
            # print (packet)

            # ID of the desired operation
            operation_id = packet[0]

            # The total length of payload (length of topic, topic content and raw_data)
            payload_len = packet[1]

            # Manage payload content depending on payload len
            if not payload_len:
                payload = 0

            else:
                # Total payload contents
                payload = packet[2:payload_len+2]

                # Check for ID responding for subscribe and unsubscribe

            if operation_id == 1:
                result = Connect.deserialize_payload()
            elif operation_id == 2:
                result = Disconnect.deserialize_payload()
            elif operation_id == 3:
                result = Subscribe.deserialize_payload(payload)
            elif operation_id == 4:
                result = Unsubscribe.deserialize_payload(payload)
            elif operation_id == 5:
                result = Publish.deserialize_payload(payload)
            elif operation_id == 99:
                result = BrokerMessage.deserialize_payload(payload)
            else:
                result = Packet(operation_id=operation_id, payload=payload)

            return result

        except IndexError:
            raise WrongPacket


class Connect(Packet):
    """ Returns a packet for HVLP client connect operation. """

    operation_id = 1

    def __init__(self, payload=""):

        super(Connect, self).__init__(self.operation_id, payload)

    @classmethod
    def deserialize_payload(cls):
        """ Deserialize transferred packet to data list. """

        return cls(payload="")


class Disconnect(Packet):
    """ Returns a packet for HVLP client disconnect operation. """

    operation_id = 2

    def __init__(self, payload=""):

        super(Disconnect, self).__init__(self.operation_id, payload)

    @classmethod
    def deserialize_payload(cls):
        """ Deserialize transferred packet to data list. """

        return cls(payload="")


class Subscribe(Packet):
    """ Returns a packet for HVLP client subscribe operation. """

    operation_id = 3

    def __init__(self, topics):
        self.topics = topics
        payload = []

        # Add the topics and their length to the payload, symbol by symbol
        for topic in self.topics:
            topic_len = len(topic)
            payload.append(topic_len)
            payload.extend(topic.encode('utf-8'))

        super(Subscribe, self).__init__(self.operation_id, payload)

    @classmethod
    def deserialize_payload(cls, payload):
        """ Extract one or more topics defined in the payload. """

        topics_deque = deque(payload)
        topic_list = []
        while topics_deque:
            topic_len = int(topics_deque.popleft())
            topic = ""
            topic_letters = []
            for _ in range(topic_len):
                topic_letters.append(chr(topics_deque.popleft()))
                topic = "".join(topic_letters)
            topic_list.append(topic)

        return cls(topic_list)


class Unsubscribe(Packet):
    """ Returns a packet for HVLP client unsubscribe operation. """

    operation_id = 4

    def __init__(self, topics):
        self.topics = topics
        payload = []

        # Add the topics and their length to the payload, symbol by symbol
        for topic in self.topics:
            topic_len = len(topic)
            payload.append(topic_len)
            payload.extend(topic.encode('utf-8'))

        super(Unsubscribe, self).__init__(self.operation_id, payload)

    @classmethod
    def deserialize_payload(cls, payload):
        """ Extract one or more topics defined in the payload. """

        topics_deque = deque(payload)
        topic_list = []
        while topics_deque:
            topic_len = int(topics_deque.popleft())
            topic = ""
            topic_letters = []
            for _ in range(topic_len):
                topic_letters.append(chr(topics_deque.popleft()))
                topic = "".join(topic_letters)
            topic_list.append(topic)

        return cls(topic_list)


class Publish(Packet):
    """ Returns a packet for HVLP client publish operation. """

    operation_id = 5

    def __init__(self, topic, data):

        self.topic = str(topic)
        self.data = str(data)
        self.payload = []
        topic_len = len(self.topic)
        self.payload.append(topic_len)
        self.payload.extend(self.topic)
        self.payload.extend(self.data)

        super(Publish, self).__init__(self.operation_id, self.payload)

    @classmethod
    def deserialize_payload(cls, payload):
        """ Extract published topic and data from payload. """

        # Topic length
        topic_len = int(payload[0])

        # Topic letters taken one by one
        topic_letters = payload[1:topic_len + 1]

        # Extracted topic name
        topic = str(topic_letters)

        # Extracted data list
        data = list(payload[topic_len + 1:])

        return cls(topic, data)


class BrokerMessage(Packet):
    """ Returns a packet for HVLP broker answer. """

    operation_id = 99

    def __init__(self, message, data):

        self.message = message
        self.data = data
        self.payload = []
        message_len = len(self.message)

        # Appends total message length
        self.payload.append(message_len)

        # Appends elements of payload
        self.payload.extend(self.message.encode('utf-8'))
        if isinstance(self.data, int):
            self.payload.append(self.data)
        else:
            self.payload.extend(self.data)

        super(BrokerMessage, self).__init__(self.operation_id, self.payload)

    @classmethod
    def deserialize_payload(cls, payload):
        """ Deserialize transferred packet to data list. """

        # Message length
        message_len = int(payload[0])

        # Message letters taken one by one
        message_letters = payload[1:message_len + 1]

        # Extracted topic name
        message = str(message_letters)

        # Extracted data list
        data = list(payload[message_len + 1:])

        return cls(message, data)

###########################################################################################


def tests():
    # p1 = [78, 44, "l", "t"]
    # ds1 = Packet.deserialize(p1)
    # print (ds1.payload)
    # print (ds1.operation_id)

    p1 = Subscribe(topics=['a', 'b'])
    ser = p1.serialize()
    p2 = Packet.deserialize(ser)
    print(p1)
    print(p2)


if __name__ == "__main__":
    tests()
