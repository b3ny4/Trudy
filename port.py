
import socket

class Port():

    def __init__(self, socket: socket.socket, hostname : str):
        self.__sock = socket
        self.__hostname = hostname

    def get_version(self):
        # wait if server sends banner
        banner = self.__receive()
        if (banner):
            # TODO: get version from banner, if it actually returns the version one day
            # TODO: expect banner other than FTP
            return self.__get_version_ftp()
        else:
            # TODO: expect other services than HTTP
            return self.__get_version_http()

    def __get_version_ftp(self):
        self.__send("ACCT")
        result = self.__receive()
        if result.startswith("530"):
            return "vs-ftpd"
        if result.startswith("500"):
            return "py-ftpd"
        if result.startswith("502"):
            return "ProFTPd"
        if result.startswith("202"):
            return "Pure-FTPd"
        return ""

    def __get_version_http(self):
        self.__send("GET / HTTP/1.0")
        self.__send("HOSTNAME: " + self.__hostname)
        self.__send("")
        result = self.__receive()
        if "\r\nServer:" in result:
            for line in result.split("\r\n"):
                if line.startswith("Server: "):
                    return line.split(": ")[1].replace("/", " ")

    def __send(self, message):
        self.__sock.send(message.encode() + b"\r\n")

    def __receive(self):
        try:
            return self.__sock.recv(1024).decode()
        except (TimeoutError):
            return ""
