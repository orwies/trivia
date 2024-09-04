from consts import (
    MAX_DATA_LENGTH,
    DELIMITER,
    LENGTH_FIELD_LENGTH,
    CMD_FIELD_LENGTH,
    COMMANDS,
    ERROR_RETURN,
)


def build_message(cmd, data):
    """
    Gets command name and data field and creates a valid protocol message
    Returns: str, or None if error occured
    """
    if cmd not in COMMANDS or len(data) > MAX_DATA_LENGTH:
        return ERROR_RETURN

    cmd = cmd.ljust(CMD_FIELD_LENGTH)
    data_length = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
    message_fields = [cmd, data_length, data]
    full_msg = DELIMITER.join(message_fields)
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    if data.count(DELIMITER) < 2:
        return ERROR_RETURN, ERROR_RETURN

    message_fields = data.split(DELIMITER)
    command = message_fields[0].strip()
    if command not in COMMANDS:
        return ERROR_RETURN, ERROR_RETURN

    data_length = message_fields[1].strip()
    if not data_length.isnumeric():
        return ERROR_RETURN, ERROR_RETURN

    int_data_length = int(data_length)
    data = message_fields[2]
    if int_data_length > MAX_DATA_LENGTH or int_data_length != len(data):
        return ERROR_RETURN, ERROR_RETURN

    return command, data
