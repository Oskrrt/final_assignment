import inspect
import os
import datetime
import traceback
from functools import wraps

#LOG_FILE_PATH = os.path.join('src', 'file_organizer', 'logs', 'file_handling_logs.txt')

def logged(log_event):
    def log(func):
        # logs the file handling events to src/file_organizer/logs/file_handling_logs.txt
        # and the error events to src/file_organizer/logs/error_logs.txt
        @wraps(func)
        def wrapper(*args, **kwargs):
            if log_event == "error":
                log_file_path = os.path.join('src', 'file_organizer', 'logs', 'error_logs.txt')
            else:
                log_file_path = os.path.join('src', 'file_organizer', 'logs', 'file_handling_logs.txt')
            # generate message content based on log_event
            message_to_log = create_log_message(log_event, args)
            try:
                with open(log_file_path, "a") as log_file:
                    log_file.write(message_to_log)
                    return func(*args, **kwargs)
            except FileNotFoundError as e:
                print("File not found: " + e.filename)
                raise e
        return wrapper
    return log

def create_log_message(log_event, message_content):
    message_to_log = ""
    if log_event == "directory reset":
        message_to_log = f"{datetime.datetime.now()} - {log_event} to original state, deleted subfolders\n"
    elif log_event == "delete":
        message_to_log = f"{datetime.datetime.now()} - {log_event} file: {message_content[1]}\n"
    elif log_event == "file moved":
        message_to_log = f"{datetime.datetime.now()} - {log_event} to correct directory - file: {message_content[1]}\n"
    elif log_event == "directory created":
        message_to_log = f"{datetime.datetime.now()} - {log_event}: {message_content[1]}\n"
    elif log_event == "error":
        exc = traceback.format_exc()
        message_to_log = f"{datetime.datetime.now()} - {log_event}: {exc}\n"

    return message_to_log

# Handles errors and shuts down the execution of the program.
@logged("error")
def log_error(e, message=None):
    function_name = inspect.currentframe().f_back.f_back.f_code.co_name
    file_name = inspect.currentframe().f_back.f_back.f_code.co_filename
    message = "Error: " + repr(e) + " occurred in method: " + function_name + " in file: " + file_name
    red = '\033[91m'
    print(f"{red}" + message)
    #exit(1)
