import socket
import select
import random

from protocol.protocol import build_message, parse_message, print_menu, print_questions
from protocol.consts import (
    PROTOCOL_CLIENT,
    MAX_MSG_LENGTH,
    ERROR_RETURN,
    PROTOCOL_SERVER,
)

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

# HELPER SOCKET METHODS


def build_and_send_message(conn, command, data=""):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), command (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    global messages_to_send
    full_msg = build_message(command, data).encode()
    print("[SERVER] ", full_msg)  # Debug print
    messages_to_send.append({conn.getpeername(): full_msg})


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
    print("[CLIENT] ", full_msg)  # Debug print
    command, data = parse_message(full_msg)
    return command, data


def print_client_sockets():
    for key in logged_users:
        print(key)

# Data Loaders #


def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        2313: {
            "question": "How much is 2+2",
            "answers": ["3", "4", "2", "1"],
            "correct": 2,
        },
        4122: {
            "question": "What is the capital of France?",
            "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
            "correct": 3,
        },
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []},
    }
    return users


# SOCKET CREATOR


def setup_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Server is up and running")
    return server_socket


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, "ERROR", error_msg)
    return None


##### MESSAGE HANDLING
def create_random_question():
    questions_dict = load_questions()
    random_question_id = random.choice(list(questions_dict.keys()))
    question = questions_dict[random_question_id]["question"]
    answers_list = questions_dict[random_question_id]["answers"]
    answers = '#'.join(answers_list)
    data = f"{str(random_question_id)}#{question}#{answers}"
    return data



def handle_question_message(conn, data = None):
    build_and_send_message(conn, PROTOCOL_SERVER["your_question_msg"], create_random_question())



def handle_answer_message(conn, username, data):
    questions_dict = load_questions()
    question_id_and_answer = data.split('#')
    question_id, answer = question_id_and_answer[0], question_id_and_answer[1]
    right_answer = str(questions_dict[int(question_id)]["correct"])
    if answer == right_answer:
        users[username]["score"] += 5
        build_and_send_message(conn, PROTOCOL_SERVER["correct_answer_msg"])
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["wrong_answer_msg"], right_answer)


def handle_getscore_message(conn, data = None):
    logged_user_username = logged_users[conn.getpeername()]
    build_and_send_message(conn, PROTOCOL_SERVER["your_score_msg"], str(users[logged_user_username]["score"]))
    # Implement this in later chapters


def handle_highscore_message(conn, data = None):
    names_scores = [(name, user['score']) for name, user in users.items()]
    sorted_names_scores = sorted(names_scores, key=lambda x: x[1], reverse=True)
    result = str(', '.join(f"{name}: {score}" for name, score in sorted_names_scores))
    build_and_send_message(conn, PROTOCOL_SERVER["all_score_message"], result)



def handle_logged_message(conn, data = None):
    result = ''.join(str(value) for value in logged_users.values())
    build_and_send_message(conn, PROTOCOL_SERVER["logged_answer_msg"], result)



def handle_logout_message(conn, data = None):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    del logged_users[conn.getpeername()]
    conn.close()

    # Implement code ...


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later
    username_and_password = data.split("#", maxsplit=1)
    username = username_and_password[0]
    password = username_and_password[1]
    if username in users.keys():
        if password == users[username]["password"]:
            if username in logged_users.values():
                send_error(conn, "user already logged!")
                return None
            build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"])
            logged_users.update({conn.getpeername(): username})
            return None
    send_error(conn, "password or username is incorrect!")
    return None

    # Implement code ...


CMD_FUNCTION_DICTIONARY = {
    PROTOCOL_CLIENT["login_msg"]: handle_login_message,
    PROTOCOL_CLIENT["logout_msg"]: handle_logout_message,
    PROTOCOL_CLIENT["my_score_msg"]: handle_getscore_message,
    PROTOCOL_CLIENT["highscore_msg"]: handle_highscore_message,
    PROTOCOL_CLIENT["logged_msg"]: handle_logged_message,
    PROTOCOL_CLIENT["get_question_msg"]: handle_question_message,
    PROTOCOL_CLIENT["send_answer_msg"]: handle_answer_message
}



def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users  # To be used later
    if cmd != PROTOCOL_CLIENT["login_msg"] and conn.getpeername() not in logged_users:
        send_error(conn, "you must login before you start to play!")
        return None
    if cmd not in CMD_FUNCTION_DICTIONARY:
        send_error(conn, "enter a valid command!")
        return None
    CMD_FUNCTION_DICTIONARY[cmd](conn, data)
    if cmd == PROTOCOL_CLIENT["get_question_msg"]:
            command, answer_status_and_answer = recv_message_and_parse(conn)
            CMD_FUNCTION_DICTIONARY[PROTOCOL_CLIENT["send_answer_msg"]](conn,
            logged_users[conn.getpeername()], answer_status_and_answer)
    return None
    # Implement code ...


def main():
# Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    users = load_user_database()
    print("Welcome to Trivia Server!")

    # Implement code ...
    server_socket = setup_socket()
    while True:
        (client_socket, client_address) = server_socket.accept()
        print(f"Connection from {client_address} has been established.")
        while True:
            try:
                command, data = recv_message_and_parse(client_socket)
                if command == None or data == None:
                    handle_logout_message(client_socket)
                    break
                handle_client_message(client_socket, command, data)
                if command == PROTOCOL_CLIENT["logout_msg"]:
                    break
            except socket.error:
                del logged_users[client_socket.getpeername()]
                print(f"client {client_address} disconnected.")

if __name__ == "__main__":
    main()