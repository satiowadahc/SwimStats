"""
Network.py

   Data Recording of swimming stats

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""
import socket
from PyQt5 import QtCore


class Snooper(QtCore.QObject):
    """
    Network Listener for Messages on the network from any Omnisport 2000
    """
    message = QtCore.pyqtSignal(int, str)

    def __init__(self):
        QtCore.QObject.__init__(self)
        udp_ip = "0.0.0.0"
        udp_port = 21000

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((udp_ip, udp_port))
        self.working = True

    def run(self):
        """
        QtCore Thread for multitasking
        """
        print("Network Started")
        while self.working:
            data, _ = self.sock.recvfrom(1024)
            # https://timingguys.com/topic/daktronics-rtd-protocol-reference?reply=588895125796619801#7507031073
            # <SYN> + HEADER + <SOH> + CONTROL + <STX> + TEXT + <EOT> + SUM + <ETB>
            # 0x16 + 20000000 + 0x01 + 004010<offset> + 0x02 + TEXT + 0x04 + CHECKSUM + 0x17
            # print(f"received message: {data} Length: {len(data)}")
            if len(data) >= 34:
                control, useful = data.split(b"\x02")
                offset = control[-4:]
                message = useful.split(b"\x17")[0][:-4]
                # print("Offset", offset, "Data", message)
                self.message.emit(int(offset), message.decode('utf-8'))

    def stop(self):
        """Stop the thread"""
        self.working = False


class FakeOmnisport:
    """
    Fake Messages from Daktronics Omnisport 2000
    """

    def __init__(self):
        self.udp_ip = "127.0.0.1"
        self.udp_port = 21000
        message = b"Hello, World!"

        print(f"UDP target IP: {self.udp_ip}")
        print(f"UDP target port: {self.udp_port}")
        print(f"message: {self.udp_port}")

        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        self.sock.sendto(message, (self.udp_ip, self.udp_port))

    def send(self, msg):
        """Send Message to the network"""
        self.sock.sendto(msg, (self.udp_ip, self.udp_port))

    def fake_race(self, msg):
        """ TODO: Send fake race data"""
        raise NotImplementedError


if __name__ == '__main__':
    testSnooper = Snooper()
