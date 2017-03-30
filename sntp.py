import argparse
import socket
import threading
from ntp_client import NTPClient


def run_server(delay, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", port))
        sock.listen(10)

        while True:
            connection, address = sock.accept()
            print("connected " + str(address))
            connection.recv(1024)
            thread = threading.Thread(target=handle_connection, args=(delay, connection))
            thread.start()


def handle_connection(delay, connection):
    error, packet, arrive_time = NTPClient.send_packet("pool.ntp.org", 123, 2)

    if not error == NTPClient.NO_ERRORS:
        connection.sendall(b"Server error")

    packet.reference += delay
    packet.receive += delay
    packet.transmit += delay

    connection.sendall(packet.pack())


if __name__ == "__main__":
    print("SNTP server started")

    parser = argparse.ArgumentParser(description="Deceiving sntp server")
    parser.add_argument("-d", "--delay", type=int, default=5, help="delay")
    parser.add_argument("-p", "--port", type=int, default=123, help="port")
    args = parser.parse_args()

    run_server(args.delay, args.port)
