# Protocol Constants
class CustomException(Exception):
    def __init__(self):
        message = f"An error has happened according to protocol"
        super().__init__(message)
