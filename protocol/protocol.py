from click import command


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


# Protocol Messages
# In this dictionary we will have all the client and server command names
commands_dict = {
    "LOGIN": {
        "parameters": {"name": "username", "name": "password"},
        "message": {"enter name and password divided by #"},
        "SEND_ANSWER": {"parameters": {"name": "id", "name": "choice"}},
        "MY_SCORE": {"parameters": {}},
    }
}

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    message_fields = {}
    if proper_command(cmd):
        message_fields.append(cmd)
        message_length = len(data)
        message_fields.append(message_length)
        message_fields.append(data)
        full_msg = join_data(message_fields)
        return full_msg
    return None
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    # Implement code ...


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    # Implement code ...
    message_fields = data.split("|")
    command = message_fields[0]
    data_length = int(message_fields[1])
    data = message_fields[2]
    if proper_command(command):
        if 0 <= data_length < 10000 and proper_parameters(command, data):
            return command, data
    return None, None
    # The function should return 2 values

    return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    max_split = expected_fields - 1
    string_list = msg.split("#", max_split)
    return string_list


# Implement code ...


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    # Implement code ...
    separator = "|"
    joined_items = separator.join(msg_fields)
    return joined_items


def proper_command(command):
    for key, inner_dict in commands_dict.items():
        if command in inner_dict.values():
            return True
        return False


def proper_parameters(command, data):
    parameters = commands_dict[command]["parameters"]
    number_of_parameters = len(parameters)
    number_of_dividers = number_of_parameters - 1
    if number_of_parameters > 0:
        if "#".count(data) < number_of_dividers:
            return False
    return True
