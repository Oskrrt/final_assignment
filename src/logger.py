import inspect
import time
import os
import datetime
import traceback
from functools import wraps

def logged(log_event):
    def log(func):
        # logs the file handling events to resources
        # and the error events to resources
        @wraps(func)
        def wrapper(*args, **kwargs):
            # generate the file path
            log_file_path = create_path_to_log_file(func, log_event)
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

def create_path_to_log_file(func, log_event):
    log_file_path = None
    if log_event == "error":
        called_from_module = inspect.getmodulename(inspect.trace()[0].filename)
    else:
        called_from_module = inspect.getmodulename(inspect.getfile(func))

    if called_from_module == "route_planner":
        log_path_suffix = "tarjan_planner_logs.txt" if log_event != "error" else "error_logs.txt"
        log_file_path = os.path.join('resources', 'tarjan_planner_logs', log_path_suffix)
    elif called_from_module == "file_handler":
        log_path_suffix = "file_handling_logs.txt" if log_event != "error" else "error_logs.txt"
        log_file_path = os.path.join('resources', 'file_organizer_logs', log_path_suffix)

    return log_file_path

# Handles errors and shuts down the execution of the program.
@logged("error")
def log_error(e):
    function_name = inspect.currentframe().f_back.f_back.f_code.co_name
    file_name = inspect.currentframe().f_back.f_back.f_code.co_filename
    message = "Error: " + repr(e) + " occurred in method: " + function_name + " in file: " + file_name
    red = '\033[91m'
    print(f"{red}" + message)
    exit(1)

### function taken from Lecture7, Metaprogramming.ipynb
def time_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time of {func.__name__}: {end - start:.5f} seconds")
        return result
    return wrapper

# no need to export create_log_message
__all__ = ['logged', 'log_error', 'time_this']