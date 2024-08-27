import socket
import protocol.protocol as protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((protocol.IP, protocol.PORT))

    while True:
        user_input = input("enter a command:\n ")
        if protocol.proper_command(user_input):
            print()


if __name__ == "__main__":
    main()
