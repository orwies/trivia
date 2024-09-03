COMMANDS_DICT = {
    "CLIENT": {
        "LOGIN": {
            "parameters": [
                {"name": "username", "type": "string"},
                {"name": "password", "type": "string"},
            ],
        },
        "LOGOUT": {},
        "LOGGED": {},
        "GET_QUESTION": {},
        "SEND_ANSWER": {"parameters": ["id", "choice"]},
        "MY_SCORE": {},
        "HIGHSCORE": {},
    },
    "SERVER": {
        "LOGIN_OK": {},
        "LOGGED_ANSWER": {"parameters": ["username1", "username2"]},
        "YOUR_QUESTION": {
            "parameters": ["id", "question", "answer1", "answer2", "answer3", "answer4"]
        },
        "CORRECT_ANSWER": {},
        "WRONG_ANSWER": {"parameters": ["answer"]},
        "YOUR_SCORE": {"parameters": ["score"]},
        "ALL_SCORE": {
            "parameters": [
                {
                    "name": "users-scores",
                    "type": "list",
                    "parameters": [
                        {"name": "username", "type": "string"},
                        {"name": "scores", "type": "integer"},
                    ],
                }
            ]
        },
    },
}

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
}  # ..  Add more commands if needed

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = (
    10**LENGTH_FIELD_LENGTH - 1
)  # Max size of data field according to protocol
MSG_HEADER_LENGTH = (
    CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1
)  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
