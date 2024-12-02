import os
import datetime
from functools import wraps




def logged(log_event, file=None, message=None):
    def log(func):
        if log_event == "error":
            log_file_path = os.path.join('src', 'file_organizer', 'logs', 'error_logs.txt')
        else:
            log_file_path = os.path.join('src', 'file_organizer', 'logs', 'file_handling_logs.txt')
        # logs the message sending event to resources/message_logs.txt
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"{datetime.datetime.now()} - {log_event}: on file {file} {message}\n")
            except FileNotFoundError as e:
                print("File not found: " + e.filename)
                raise e
        return wrapper
    return log