import socket
import sys
import time
from ntp_packet import NTPPacket
from ntp_client import NTPClient


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", 123))
        sock.sendall(b"give me time plz")
        data = sock.recv(1024)
        arrive_time = time.time() + NTPClient.FORMAT_DIFF
        packet = NTPPacket()

        try:
            packet.unpack(data)
        except Exception:
            print("Server error")
            sys.exit()

        print(packet.to_display())
        print("Time difference: " + str(packet.get_time_different(arrive_time)))
