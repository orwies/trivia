import socket
from protocol.protocol import build_message, parse_message
from protocol.consts import PROTOCOL_CLIENT, MAX_MSG_LENGTH, ERROR_RETURN

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS


def build_and_send_message(conn, command, data=""):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), command (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    full_msg = build_message(command, data)
    conn.send(full_msg.encode())


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: command (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    # ..
    full_msg = conn.recv(MAX_MSG_LENGTH).decode()
    command, data = parse_message(full_msg)
    return command, data


def build_send_recv_parse(conn, command, data=""):
    # implemenet
    build_and_send_message(conn, command, data)
    return recv_message_and_parse(conn)


def connect():
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def login(conn):
    username = input("Please enter username:\n")
    password = input("Please enter password:\n")
    data = f"{username}#{password}"
    command, _ = build_send_recv_parse(conn, PROTOCOL_CLIENT["login_msg"], data)
    print(command)
    return command


def logout(conn):
    # Implement code
    build_send_recv_parse(conn, PROTOCOL_CLIENT["logout_msg"])


def main():
    # Implement code
    while True:
        my_socket = connect()
        while True:
            command = input("Please enter a command:\n")
            if command == PROTOCOL_CLIENT["login_msg"]:
                login_result = login(my_socket)
                if login_result == ERROR_RETURN:
                    my_socket.close()
                    break
            if command == PROTOCOL_CLIENT["logout_msg"]:
                logout(my_socket)
                break


if __name__ == "__main__":
    main()
