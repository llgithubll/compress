"""
检测压缩算法的准确性, 评估压缩率, 效率
"""
import time

from bitio import BitReader
from RunLength import RunLength
from Huffman import Huffman


class FileBits:
    def __init__(self, fp):
        self.f = open(fp, 'rb')
        self.bit_stream = BitReader(self.f)
        self.bits = []
        while True:
            x = self.bit_stream.read_bit()
            if not self.bit_stream.read:
                break
            self.bits.append(x)

    def __eq__(self, other):
        if len(self.bits) != len(other.bits):
            return False
        return self.bits == other.bits

    def __repr__(self):
        b = ['1' if x else '0' for x in self.bits]
        return ''.join(b)

    def __len__(self):
        return len(self.bits)

    def __del__(self):
        self.f.close()


def test_compress_expand(ori_files, com_files, exp_files, algs):
    for of, cf, ef in zip(ori_files, com_files, exp_files):
        b_com = time.time()
        algs.compress(of, cf)  # 压缩, origin -> compress
        e_com = time.time()
        algs.expand(cf, ef)  # 解压缩, compress -> origin
        e_exp = time.time()
        of_bits, cf_bits, ef_bits = FileBits(of), FileBits(cf), FileBits(ef)
        print(of)
        print('len', len(of_bits), '->', len(cf_bits), 'rate', len(cf_bits) / len(of_bits))
        print('compress {}s, expand {}s'.format(e_com - b_com, e_exp - e_com))
        assert of_bits == ef_bits  # origin bits == expand bits
        print()


def test_run_length():
    print('-' * 30, 'RunLength', '-' * 30)
    ori_files = ['data/4runs.bin',
                 'data/abra.txt',
                 'data/q32x48.bin',
                 'data/q64x96.bin']
    com_files = ['temp_files/4runs.bin.rl',
                 'temp_files/abra.txt.rl',
                 'temp_files/q32x48.bin.rl',
                 'temp_files/q64x96.bin.rl']
    exp_files = ['temp_files/4runs.bin',
                 'temp_files/abra.txt',
                 'temp_files/q32x48.bin',
                 'temp_files/q64x96.bin']
    test_compress_expand(ori_files, com_files, exp_files, RunLength)


def test_huffman():
    print('-' * 30, 'Huffman', '-' * 30)
    ori_files = ['data/4runs.bin',
                 'data/abra.txt',
                 'data/q32x48.bin',
                 'data/q64x96.bin',
                 'data/tinytinyTale.txt',
                 'data/tinyTale.txt',
                 'data/medTale.txt',
                 'data/tale.txt']
    com_files = ['temp_files/4runs.bin.huffman',
                 'temp_files/abra.txt.huffman',
                 'temp_files/q32x48.bin.huffman',
                 'temp_files/q64x96.bin.huffman',
                 'temp_files/tinytinyTale.txt.huffman',
                 'temp_files/tinyTale.txt.huffman',
                 'temp_files/medTale.txt.huffman',
                 'temp_files/tale.txt.huffman']
    exp_files = ['temp_files/4runs.bin',
                 'temp_files/abra.txt',
                 'temp_files/q32x48.bin',
                 'temp_files/q64x96.bin',
                 'temp_files/tinytinyTale.txt',
                 'temp_files/tinyTale.txt',
                 'temp_files/medTale.txt',
                 'temp_files/tale.txt']
    test_compress_expand(ori_files, com_files, exp_files, Huffman)


if __name__ == '__main__':
    test_run_length()
    test_huffman()
