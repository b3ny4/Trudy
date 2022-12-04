import sys
import os
import subprocess
from threading import Thread, Lock
from .logger import Logger
import scapy.all as scapy
import netfilterqueue

class Trudy():

    def __init__(self, logger : Logger = Logger()):
        self.__logger = logger
        self.__server = None

        
    def sniff(self, interface, callback):
        scapy.sniff(iface=interface, store=False, prn=callback)

    def enforce_sudo(self):
        if os.getuid() != 0:
            ret = subprocess.check_call(f"sudo $(which python3) {' '.join(sys.argv)}", shell=True)
            exit()
        if os.getuid() != 0:
            self.__logger.log("Run script as root!", self.__logger.Level.FAIL)
            exit()

    def use_iface(self, iface : str):
        scapy.conf.iface = iface
    
    def enable_netfilter_queue(self, callback):
        # TODO: use nftables
        ret = subprocess.check_call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
        ret += subprocess.check_call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)
        ret += subprocess.check_call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
        if ret != 0:
            self.__logger.log("Unable to enable netfilter queue", self.__logger.Level.FAIL)
            return
        self.__logger.log("Netfilter Queue Enabled", self.__logger.Level.SUCCESS)
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, callback)
        queue.run()

    def reset_firewall(self):
        # TODO: use nftables
        ret = subprocess.check_call(f"iptables --flush", shell=True)
        if ret != 0:
            self.__logger.log("Unable to reset firewall", self.__logger.Level.FAIL)
            return
        self.__logger.log("Firewall reset", self.__logger.Level.SUCCESS)

    def __start_server(self):
        ret = subprocess.check_call(f"$(which python3) -m http.server 8000", shell=True)

    def start_server(self):
        if self.__server != None:
            self.__logger.log("Server already started." ,self.__logger.Level.INFO)
            return
        self.__server = Thread(target=self.__start_server)
        self.__server.start()
        self.__logger.log("Server started.", self.__logger.Level.SUCCESS)

    def enable_packet_forwarding(self):
        try:
            with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
                f.write("1")
            self.__logger.log("Packet Forwarding Enabled")
        except IOError:
            self.__logger.log("Error enabling packet forwarding")

    def disable_packet_forwarding(self):
        try:
            with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
                f.write("0")
            self.__logger.log("Packet Forwarding Disabled")
        except IOError:
            self.__logger.log("Error disabling port forwarding")