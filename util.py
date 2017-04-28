import struct
import io

class xFile(io.FileIO):

    def read_int(self, le=True):
        """
        Read and return signed 32-bit value from the currently opened binary file.
        
        le  If True, the LSB is the first byte read. If False, the MSB is the first byte read.
        """
        if le:
            return struct.unpack("<i", self.read(4))[0]
        else:
            return struct.unpack(">i", self.read(4))[0]

    def write_int(self, value, le=True):
        if le:
            self.write(struct.pack("<i", value))
        else:
            self.write(struct.pack(">i", value))

    def read_short(self, le=True):
        """
        Read and return signed 16-bit value from the currently opened binary file.

        le  If True, the LSB is the first byte read. If False, the MSB is the first byte read.
        """
        if le:
            return struct.unpack("<h", self.read(2))[0]
        else:
            return struct.unpack(">h", self.read(2))[0]

    def read_float(self, le=True):
        if le:
            return struct.unpack("<f", self.read(4))[0]
        else:
            return struct.unpack(">f", self.read(4))[0]

    def read_unsigned_int(self, le=True):
        if le:
            return struct.unpack("<I", self.read(4))[0]
        else:
            return struct.unpack(">I", self.read(4))[0]

    def read_unsigned_short(self, le=True):
        if le:
            return struct.unpack("<H", self.read(2))[0]
        else:
            return struct.unpack(">H", self.read(2))[0]

    def read_byte(self):
        return struct.unpack("B", self.read(1))[0]