from ntp_client import NTPClient
import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NTP client (2-4 protocol version)")
    parser.add_argument("-s", "--server", type=str, default="pool.ntp.org", help="NTP server")
    parser.add_argument("-v", "--version", type=int, default=2, help="NTP version")
    parser.add_argument("-p", "--port", type=int, default=123, help="port")
    parser.add_argument("-d", "--debug", action="store_true", help="debug mode")
    args = parser.parse_args()

    result = NTPClient.get_information_from_server(args.server, args.port, args.version, debug_mode=args.debug)
    print(result)
