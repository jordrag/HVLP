""" HVLP client's data taken from console. """

# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals

import sys
import threading
import time

sys.path.append(str("."))
sys.path.append(str(".."))


class MenuHVLP(object):
    """
    Defining possible choices for an action from client to the broker.

    Attributes:
        operation_id: int
            ID for defined operations in HVLP.

    """

    def __init__(self, client):
        self.operation_id = int
        self.lock = threading.Lock()
        self.client = client
        self.connected_flag = False

    def lock_print(self, *args, **kwargs):
        """ Locks console for printing."""

        self.lock.acquire()
        print(*args, **kwargs)
        self.lock.release()

    def choice(self):
        """ Choices manager. """

        menu = """      ***** Client's commands *****

          0: stop client
          1: connect to server
          2: disconnect from server
          3: subscribe to topic
          4: unsubscribe to topic
          5: publish data to topic

               """

        while True:
            time.sleep(0.1)
            self.lock_print(menu)

            commands = {0: "",
                        1: self.client.connect,
                        2: self.client.disconnect,
                        3: self.client.subscribe,
                        4: self.client.unsubscribe,
                        5: self.client.publish
                        }

            while True:
                try:
                    self.operation_id = input("Make your choice (0-5): ")

                    if self.operation_id in commands.keys():
                        break
                    else:
                        print("Please choose legal operation ID !")

                except NameError:
                    print("Only numbers please !")

                except SyntaxError:
                    print("Please choose legal operation ID !")

            if self.operation_id == 0:
                if self.connected_flag:
                    result = commands[2]()
                break
            elif self.operation_id == 3 or self.operation_id == 4:
                topics_list = self.take_topics()
                result = commands[self.operation_id](topics_list)
            elif self.operation_id == 5:
                topic, data = self.publish_data()
                result = commands[self.operation_id](topic, data)
            else:
                self.connected_flag = True
                result = commands[self.operation_id]()

            self.client.send_packet(result)

    def take_topics(self):
        """ Takes topics from user on console. """

        topics_list = []

        while True:
            mes = "Please enter a topic, for quit <#stop>: "
            self.lock_print(mes)
            topic = raw_input()
            if topic == "#stop":
                break
            topics_list.append(topic)

        return topics_list

    def publish_data(self):
        """ Takes data for publishing from client on console."""

        mes = "Please enter a topic: "
        self.lock_print(mes)
        topic = raw_input()

        mes = "Please enter data to be send: "
        self.lock_print(mes)
        data = raw_input()

        return topic, data
