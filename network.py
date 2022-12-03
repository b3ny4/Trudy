import scapy.all as scapy

from .logger import Logger
from .client import Client

class Network():
    def __init__(self, ip : str, netmask : int, logger : Logger = Logger()):
        self.__ip = f"{ip}/{netmask}"
        self.__logger = logger

    def __str__(self):
        return self.__ip

    def get_clients(self):
        # create layer 3 ARP package
        arp_request = scapy.ARP(pdst=self.__ip)

        # pack ARP Request to layer 2 frame
        frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/arp_request
        self.__logger.log(frame.summary())

        # send packet
        answered_frames = scapy.srp(frame, timeout=1, verbose=False)[0]
        return [Client(frame[1].psrc, frame[1].hwsrc, logger=self.__logger) for frame in answered_frames]