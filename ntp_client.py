from ntp_packet import NTPPacket

import socket
import datetime
import time


class NTPClient:
    FORMAT_DIFF = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600
    # Waiting time for recv (seconds)
    WAITING_TIME = 5

    NO_ERRORS = 0
    SERVER_DIDNT_RESPOND_ERROR = 1
    WRONG_SERVER_ERROR = 2

    @staticmethod
    def send_packet(server, port, version):
        packet = NTPPacket(transmit=time.time() + NTPClient.FORMAT_DIFF)
        answer = NTPPacket(version_number=version)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(NTPClient.WAITING_TIME)
            s.sendto(packet.pack(), (server, port))
            data = s.recv(48)
            arrive_time = time.time() + NTPClient.FORMAT_DIFF
            answer.unpack(data)

        return answer, arrive_time

    @staticmethod
    def get_information_from_server(server="pool.ntp.org", port=123, version=2, debug_mode=False):
        try:
            packet, arrive_time = NTPClient.send_packet(server=server, port=port, version=version)
        except socket.timeout:
            return NTPClient.SERVER_DIDNT_RESPOND_ERROR, ""
        except socket.gaierror:
            return NTPClient.WRONG_SERVER_ERROR, ""

        time_different = packet.get_time_different(arrive_time)
        result = "Time different: {}\nServer time: {}".format(
                            time_different,
                            datetime.datetime.fromtimestamp(time.time() + time_different).strftime("%c"))
        if debug_mode:
            result += "\n" + packet.to_display()
        return NTPClient.NO_ERRORS, result
