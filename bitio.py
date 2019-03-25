"""
比特流的读写
"""


class BitWriter(object):
    def __init__(self, f):
        self.accumulator = 0
        self.bcount = 0
        self.out = f

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()

    def __del__(self):
        try:
            self.flush()
        except ValueError:  # I/O operation on closed file.
            pass

    def write_bit(self, bit):
        if self.bcount == 8:
            self.flush()
        if bit:
            self.accumulator |= 1 << 7 - self.bcount
        self.bcount += 1

    def write_bits(self, bits, n):
        while n > 0:
            self.write_bit(bits & 1 << n - 1)
            n -= 1

    def flush(self):
        self.out.write(bytearray([self.accumulator]))
        self.accumulator = 0
        self.bcount = 0


class BitReader(object):
    def __init__(self, f):
        self.input = f
        self.accumulator = 0
        self.bcount = 0
        self.read = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read_bit(self):
        if not self.bcount:
            a = self.input.read(1)
            if a:
                self.accumulator = ord(a)
            self.bcount = 8
            self.read = len(a)
        rv = (self.accumulator & (1 << self.bcount - 1)) >> self.bcount - 1
        self.bcount -= 1
        return rv

    def read_bits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.read_bit()
            n -= 1
        return v


if __name__ == '__main__':
    with open('temp_files/bitio_test.dat', 'wb') as outfile:
        with BitWriter(outfile) as writer:
            chars = '12345abcde'
            for ch in chars:
                writer.write_bits(ord(ch), 7)
            cnt = 98
            writer.write_bits(cnt, 7)

    with open('temp_files/bitio_test.dat', 'rb') as infile:
        with BitReader(infile) as reader:
            chars = []
            while True:
                x = reader.read_bits(7)
                if not reader.read:  # End-of-file?
                    break
                chars.append(chr(x))
            print(''.join(chars))
