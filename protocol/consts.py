PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_msg": "LOGGED",
    "get_question_msg": "GET_QUESTION",
    "send_answer_msg": "SEND_ANSWER",
    "my_score_msg": "MY_SCORE",
    "highscore_msg": "HIGHSCORE",
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "logged_answer_msg": "LOGGED_ANSWER",
    "your_question_nsg": "YOUR_QUESTION",
    "correct_answer_msg": "CORRECT_ANSWER",
    "wrong_answer_msg": "WRONG_ANSWER",
    "your_score_msg": "YOUR_SCORE",
    "login_failed_msg": "ERROR",
}
COMMANDS = [
    "LOGIN",
    "LOGOUT",
    "LOGGED",
    "GET_QUESTION",
    "SEND_ANSWER",
    "MY_SCORE",
    "HIGHSCORE",
    "LOGIN_OK",
    "ALL_SCORE",
    "LOGGED_ANSWER",
    "YOUR_QUESTION",
    "CORRECT_ANSWER",
    "WRONG_ANSWER",
    "YOUR_SCORE",
    "ERROR",
    "NO_QUESTIONS",
]
ERROR_RETURN = None  # What is returned in case of an error
COMMAND_FIELD_LENGTH = 16  # Exact length of command field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = (
    10**LENGTH_FIELD_LENGTH - 1
)  # Max size of data field according to protocol
MSG_HEADER_LENGTH = (
    COMMAND_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1
)  # Exact size of header (COMMAND+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
