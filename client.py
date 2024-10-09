import socket
from protocol.protocol import build_message, parse_message, print_menu
from protocol.consts import PROTOCOL_CLIENT, MAX_MSG_LENGTH, ERROR_RETURN, PROTOCOL_SERVER

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

def get_score(conn):
    command, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["my_score_msg"])
    if command == "YOUR_SCORE":
        return data
    else:
        return ERROR_RETURN

def get_highscore(conn):
    _, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["highscore_msg"])
    return data

def play_question(conn):
    command, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_question_msg"])
    if command == PROTOCOL_SERVER["no_questions_msg"]:
        conn.close()
    elif command == ERROR_RETURN:
        print("didn't enter a valid answer!")
        return ERROR_RETURN
    else:
        parts = data.split('#')
        question_id = parts[0]
        question = parts[1]
        print(question)
        answer_options = [
    ('1', parts[2]),
    ('2', parts[3]),
    ('3', parts[4]),
    ('4', parts[5])
]
        print(answer_options)
        return question_id 
        
def send_answer(conn, question_id, answer_choice):
    id_and_choice = f"{question_id}#{answer_choice}"
    command, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_question_msg"], id_and_choice)
    if command == PROTOCOL_SERVER["wrong_answer_msg"]:
        print(f"Nope, correct answer is {data}")
    else:
        print("YES!!!!")

def get_logged_users(conn):
    _, logged_users = build_send_recv_parse(conn, PROTOCOL_CLIENT["logged_msg"])
    print(logged_users)


def main():
    # Implement code
    while True:
        my_socket = connect()
        while True:
            login_result = login(my_socket)
            if login_result == ERROR_RETURN:
                my_socket.close()
                break
            else:
                while True:
                    print_menu()
                    command_choice = input("please enter your choice: ")
                    if command_choice == "p":
                        question_id = play_question
                        answer_choice = input("please enter your answer [1-4]: ")
                        send_answer(my_socket, question_id, answer_choice)
                    if command_choice == "s":
                        my_score_result = get_score(my_socket)
                        if my_score_result == ERROR_RETURN:
                            print("an error occurred!")
                        else:
                            print(my_score_result)
                    if command_choice == "h":
                        highscore = get_highscore(my_socket)
                        print(highscore)
                    if command_choice == "l":
                        get_logged_users(my_socket)
                    if command_choice == "q":
                        logout(my_socket)
                        break
            


if __name__ == "__main__":
    main()
