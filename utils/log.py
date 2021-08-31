import inspect
import multiprocessing
import sys
import threading
from time import time

from config import DEBUG_MODE, EASYGIF_VERSION


def clear_log():
    with open("easygif.log", "w", encoding="utf8") as out:
        out.write("-- EASYGIF DEBUG LOG --\n\n")
        out.write("© Anime no Sekai, 2021\n\n")


def write_log(new_line: str):
    """Writing out the log, wether it's to the log stack or the log file"""
    #new_line = str(new_line).replace("\n", " ")
    new_line = str(new_line)
    if DEBUG_MODE:
        with open("easygif.log", "a", encoding="utf8") as out:
            out.write(str(new_line) + "\n")


class LogLevel():
    def __init__(self, level) -> None:
        self.level = str(level)

    def __repr__(self) -> str:
        return f"<LogLevel: {self.level}>"


class LogLevels():
    INFO = LogLevel("Info")
    DEBUG = LogLevel("Debug")
    WARNING = LogLevel("Warning")
    ERROR = LogLevel("Error")

    def __repr__(self) -> str:
        return "<LogLevels Container>"


class Colors():
    NORMAL = '\033[0m'
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUEE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'


def caller_name(skip=2):
    """
    https://stackoverflow.com/a/9812105/11557354
       Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    # Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack
    return ".".join(name)


def log(message: str = "Log", step: str = None, level: LogLevel = LogLevels.DEBUG):
    write_log(
        f"{time()}｜[{level.level.upper()}] [{(step if step is not None else (caller_name() if DEBUG_MODE else 'app'))}] {message}")
    if level == LogLevels.INFO:
        print(
            f"{Colors.GREY}{int(time())}｜{Colors.NORMAL}[{level.level.upper()}] (EasyGif) [{(step if step is not None else caller_name())}] {message}")
    elif level == LogLevels.DEBUG:
        if "--debug" in sys.argv:
            print(
                f"{Colors.GREY}{int(time())}｜{Colors.NORMAL}[{level.level.upper()}] (EasyGif) [{(step if step is not None else caller_name())}] {message}")
        elif "-d" in sys.argv:
            print(
                f"{Colors.GREY}{int(time())}｜{Colors.NORMAL}[{level.level.upper()}]{Colors.GREY} (EasyGif) [{(step if step is not None else caller_name())}] {message} {Colors.NORMAL}")
    elif level == LogLevels.WARNING:
        print(
            f"{Colors.GREY}{int(time())}｜{Colors.NORMAL}[{level.level.upper()}] (EasyGif) [{(step if step is not None else caller_name())}] {Colors.YELLOW}{message}{Colors.NORMAL}")
    elif level == LogLevels.ERROR:
        print(
            f"{Colors.GREY}{int(time())}｜{Colors.NORMAL}[{level.level.upper()}] (EasyGif) [{(step if step is not None else caller_name())}] {Colors.RED}!! {message} !!{Colors.NORMAL}")


# initializing a new log session
if multiprocessing.parent_process() is None and threading.current_thread() is threading.main_thread():
    if "--clear-log" in sys.argv:
        clear_log()
    write_log(f"\n\n# Session: {time()}")
    write_log(f"EasyGif Version: {EASYGIF_VERSION}")
    write_log("")
    print(Colors.NORMAL)
    print(f"EasyGif Server v{EASYGIF_VERSION}")
    print("© Anime no Sekai, 2021")
    print()
