import inspect
import os

def custom_print(*args, **kwargs):
    # Get the caller's frame
    frame = inspect.currentframe().f_back
    # Get the file name and line number
    file_name = os.path.basename(frame.f_code.co_filename)
    line_number = frame.f_lineno
    # Print the file name and line number
    print(f"[{file_name}:{line_number}]", *args, **kwargs)