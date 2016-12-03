import struct


class NTPPacket:
    _FORMAT = "!B B b b 11I"

    def __init__(self, version_number=2, mode=3, transmit=0):
        # Necessary of enter leap second (2 bits)
        self.leap_indicator = 0
        # Version of protocol (3 bits)
        self.version_number = version_number
        # Mode of sender (3 bits)
        self.mode = mode
        # The level of "layering" reading time (1 byte)
        self.stratum = 0
        # Interval between requests (1 byte)
        self.pool = 0
        # Precision (log2) (1 byte)
        self.precision = 0
        # Interval for the clock reach NTP server (4 bytes)
        self.root_delay = 0
        # Scatter the clock NTP-server (4 bytes)
        self.root_dispersion = 0
        # Indicator of clocks (4 bytes)
        self.ref_id = 0
        # Last update time on server (8 bytes)
        self.reference = 0
        # Time of sending packet from local machine (8 bytes)
        self.originate = 0
        # Time of receipt on server (8 bytes)
        self.receive = 0
        # Time of sending answer from server (8 bytes)
        self.transmit = transmit

    def unpack(self, data: bytes):
        unpacked_data = struct.unpack(NTPPacket._FORMAT, data)

        self.leap_indicator = unpacked_data[0] >> 6  # 2 bits
        self.version_number = unpacked_data[0] >> 3 & 0b111  # 3 bits
        self.mode = unpacked_data[0] & 0b111  # 3 bits

        self.stratum = unpacked_data[1]  # 1 byte
        self.pool = unpacked_data[2]  # 1 byte
        self.precision = unpacked_data[3]  # 1 byte

        self.root_delay = get_fraction(unpacked_data[4], 16)  # 2 bytes | 2 bytes
        self.root_dispersion = get_fraction(unpacked_data[5], 16)  # 2 bytes | 2 bytes

        self.ref_id = unpacked_data[6]  # 4 bytes

        self.reference = unpacked_data[7] + unpacked_data[8] / 2 ** 32  # 8 bytes
        self.originate = unpacked_data[9] + unpacked_data[10] / 2 ** 32  # 8 bytes
        self.receive = unpacked_data[11] + unpacked_data[12] / 2 ** 32  # 8 bytes
        self.transmit = unpacked_data[13] + unpacked_data[14] / 2 ** 32  # 8 bytes

    def pack(self):
        return struct.pack(NTPPacket._FORMAT,
                           (self.leap_indicator << 6) + (self.version_number << 3) + self.mode,
                           self.stratum,
                           self.pool,
                           self.precision,
                           int(self.root_delay) + get_fraction(self.root_delay, 16),
                           int(self.root_dispersion) + get_fraction(self.root_dispersion, 16),
                           self.ref_id,
                           int(self.reference),
                           get_fraction(self.reference, 32),
                           int(self.originate),
                           get_fraction(self.originate, 32),
                           int(self.receive),
                           get_fraction(self.receive, 32),
                           int(self.transmit),
                           get_fraction(self.transmit, 32), )

    def get_time_different(self, arrive_time):
        return (self.receive - self.originate - arrive_time + self.transmit) / 2

    def to_display(self):
        return "Leap indicator: {0.leap_indicator}\n" \
                "Version number: {0.version_number}\n" \
                "Mode: {0.mode}\n" \
                "Stratum: {0.stratum}\n" \
                "Pool: {0.pool}\n" \
                "Precision: {0.precision}\n" \
                "Root delay: {0.root_delay}\n" \
                "Root dispersion: {0.root_dispersion}\n" \
                "Ref id: {0.ref_id}\n" \
                "Reference: {0.reference}\n" \
                "Originate: {0.originate}\n" \
                "Receive: {0.receive}\n" \
                "Transmit: {0.transmit}"\
                .format(self)

    def __eq__(self, other):
        return self.leap_indicator == other.leap_indicator and \
            self.version_number == other.version_number and \
            self.mode == other.mode and \
            self.stratum == other.stratum and \
            self.pool == other.pool and \
            self.precision == other.precision and \
            self.root_delay == other.root_delay and \
            self.root_dispersion == other.root_dispersion and \
            self.reference == other.reference and \
            self.originate == other.originate and \
            self.receive == other.receive and \
            self.transmit == other.transmit


def get_fraction(number, precision):
    """
    Return fraction of number with precision:
    """
    return int((number - int(number)) * 2 ** precision)
