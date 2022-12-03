from threading import Lock
import os
from termcolor import colored

class Logger():
    def __init__(self):
        self.__loading = "|/-\\"
        self.__step = 0
        self.__lock = Lock()

    class Level():
        SUCCESS = ('+', 'green')
        INFO = ('!', 'yellow')
        FAIL = ('-', 'red')
        IMPORTANT = ('!', 'magenta')

    def __clear_line(self):
        (width, _) = os.get_terminal_size()
        print(f"\r" + width * " ", end = "")

    def display_loadbar(self, message:str):
        self.__lock.acquire()
        self.__clear_line()
        self.__step += 1
        print(f"\r[{self.__loading[self.__step%len(self.__loading)]}] {message}", end="")
        self.__lock.release()

    def log(self, message:str, level:Level = Level.SUCCESS):
        self.__lock.acquire()
        self.__clear_line()
        print(colored(f"\r[{level[0]}] {message}", level[1]))
        self.__lock.release()
