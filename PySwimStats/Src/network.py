"""
Network.py

   Data Recording of swimming stats

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""
import socket
from PyQt5 import QtCore


class Snooper(QtCore.QObject):
    message = QtCore.pyqtSignal(int, str)

    def __init__(self):
        super(Snooper, self).__init__()
        UDP_IP = "0.0.0.0"
        UDP_PORT = 21000

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
        self.working = True

    def run(self):
        print("Network Started")
        while self.working:
            data, addr = self.sock.recvfrom(1024)
            # https://timingguys.com/topic/daktronics-rtd-protocol-reference?reply=588895125796619801#7507031073
            # <SYN> + HEADER + <SOH> + CONTROL + <STX> + TEXT + <EOT> + SUM + <ETB>
            # 0x16 + 20000000 + 0x01 + 004010<offset> + 0x02 + TEXT + 0x04 + CHECKSUM + 0x17
            # print(f"received message: {data} Length: {len(data)}")
            try:
                if len(data) >= 34:
                    control, useful = data.split(b"\x02")
                    offset = control[-4:]
                    message = useful.split(b"\x17")[0][:-4]
                    # print("Offset", offset, "Data", message)
                    self.message.emit(int(offset), message.decode('utf-8'))
            except Exception as e:
                print(e)



class FakeOmnisport:
    def __init__(self):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 21000
        MESSAGE = b"Hello, World!"

        print("UDP target IP: %s" % UDP_IP)
        print("UDP target port: %s" % UDP_PORT)
        print("message: %s" % MESSAGE)

        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


if __name__ == '__main__':
    testSnooper = Snooper()

