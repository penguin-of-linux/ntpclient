import argparse
import socket
import threading

from ntp_client import NTPClient
from ntp_packet import NTPPacket, UnpackError


def run_server(delay, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.bind(("127.0.0.1", port))
        except Exception:
            print("Can not create server (sure port is free)")
            return

        while True:
            data, address = sock.recvfrom(1024)

            print("Connected: ", address)

            try:
                packet = NTPPacket().unpack(data)
            except UnpackError:
                print("Wrong packet format")
                sock.sendto(b"Wrong packet format", address)
                continue

            thread = threading.Thread(target=handle_connection, args=(packet, sock, address, delay))
            thread.start()


def handle_connection(packet, sock, address, delay):
    error, packet, arrive_time = NTPClient.send_packet("pool.ntp.org", 123, 2, packet)

    if not error == NTPClient.NO_ERRORS:
        sock.sendto(b"Server error", address)

    packet.reference += delay
    packet.receive += delay
    packet.transmit += delay

    sock.sendto(packet.pack(), address)


if __name__ == "__main__":
    print("SNTP server started")

    parser = argparse.ArgumentParser(description="Deceiving sntp server")
    parser.add_argument("-d", "--delay", type=int, default=5, help="delay")
    parser.add_argument("-p", "--port", type=int, default=123, help="port")
    args = parser.parse_args()

    run_server(args.delay, args.port)
