import unittest
import ntp_client
import ntp_packet
import mock
import time


class PseudoPacket(ntp_packet.NTPPacket):
    def __init__(self):
        super().__init__()
        self.leap_indicator = 0
        self.version_number = 2
        self.mode = 4
        self.stratum = 2
        self.pool = 3
        self.precision = -20
        self.root_delay = 0
        self.root_dispersion = 0
        self.ref_id = 1223521526
        self.reference = 3687512849.4502788
        self.originate = 3687513032.6360064
        self.receive = 3687513030.383561
        self.transmit = 3687513030.383736


class TestNTPClient(unittest.TestCase):
    def test_get_information(self):
        with mock.patch("ntp_client.NTPClient.send_packet") as client_mock:
            with mock.patch("time.time") as time_mock:
                packet = PseudoPacket()
                packet.originate = 0
                packet.receive = 0
                packet.transmit = 0
                client_mock.return_value = packet, 0
                time_mock.return_value = 0
                error, information = ntp_client.NTPClient.get_information_from_server()

        right_information = "Time different: 0.0\nServer time: Thu Jan  1 05:00:00 1970"
        self.assertEqual(right_information, information)

    def test_errors(self):
        error, result = ntp_client.NTPClient.get_information_from_server("pool.ntp.org")
        self.assertEqual(ntp_client.NTPClient.NO_ERRORS, error, "No errors")

        error, result = ntp_client.NTPClient.get_information_from_server("google.com")
        self.assertEqual(ntp_client.NTPClient.SERVER_DIDNT_RESPOND_ERROR, error, "Server didnt respond")

        error, result = ntp_client.NTPClient.get_information_from_server("abrakadabra")
        self.assertEqual(ntp_client.NTPClient.WRONG_SERVER_ERROR, error, "Wrong server")


class TestNTPPacket(unittest.TestCase):
    def test_pack_unpack(self):
        packet = PseudoPacket()
        other_packet = ntp_packet.NTPPacket()
        other_packet.unpack(packet.pack())

        self.assertEqual(packet, other_packet)

    def test_get_time_different(self):
        packet = PseudoPacket()
        packet.receive = 1004
        packet.transmit = 1005

        packet.originate = 1000
        arrive_time = 1003
        self.assertEqual(3, packet.get_time_different(arrive_time), "3 seconds different(lag)")

        packet.originate = 1003
        arrive_time = 1006
        self.assertEqual(0, packet.get_time_different(arrive_time), "0 seconds different(lag)")

        packet.originate = 1006
        arrive_time = 1009
        self.assertEqual(-3, packet.get_time_different(arrive_time), "-3 seconds different(fast)")

if __name__ == "__main__":
    unittest.main()
