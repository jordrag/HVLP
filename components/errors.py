""" Raising custom errors module. """


class HVLPErrors(Exception):

    def __init__(self, main_message, extended_info):
        self.main_message = main_message
        self.extended_info = extended_info

    def __str__(self):
        if self.extended_info:
            result = self.main_message + " : " + self.extended_info
        else:
            result = self.main_message

        return result


class NotConnectedError(HVLPErrors):

    def __init__(self, message="The socket is closed, start the program again !"):
        super(NotConnectedError, self).__init__(
            main_message="Connection Error",
            extended_info=message
        )


class WrongPacket(HVLPErrors):
    def __init__(self):
        super(WrongPacket, self).__init__(
            main_message="Received wrong or bad HVLP packet !",
            extended_info=""
        )


###################################################################################################

# def test_base():
#
#     error = None
#
#     try:
#         raise NotConnectedError
#
#     except HVLPErrors as e:
#         error = e
#         print(e)
#
#     finally:
#         assert(error.base == NotConnectedError().base)
#
#
# def test_extended():
#
#     error = None
#     message = "test"
#
#     try:
#         raise NotConnectedError(message=message)
#
#     except HVLPErrors as e:
#         error = e
#         print(e)
#
#     finally:
#         assert (error.extended == message)
#
#
# if __name__ == "__main__":
#     test_base()
#     test_extended()
