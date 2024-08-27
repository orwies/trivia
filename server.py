def setup_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((protocol.IP, protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    return server_socket


def main():
    server_socket = setup_server()
    while True:
        (client_socket, client_address) = server_socket.accept()
        print("Client connected")

        while True:
            data = client_socket.recv(protocol.CMD_FIELD_LENGTH).decode()
            extracted_command = protocol.receive_command(data)
            create_server_response(extracted_command, commands_dict)


if __name__ == "__main__":
    main()
