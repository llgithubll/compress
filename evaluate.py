"""
检测压缩算法的准确性, 评估压缩率, 效率
"""
from bitstring import BitStream
from RunLength import RunLength


class FileBits:
    def __init__(self, fp):
        self.bits = BitStream(open(fp, 'rb').read())

    def __eq__(self, other):
        return self.bits == other.bits

    def __len__(self):
        return len(self.bits)

    def __repr__(self):
        return self.bits.bin


def test_run_length():
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
    for of, cf, ef in zip(ori_files, com_files, exp_files):
        RunLength.compress(of, cf)  # 压缩, origin -> compress
        RunLength.expand(cf, ef)  # 解压缩, compress -> origin
        of_bits, cf_bits, ef_bits = FileBits(of), FileBits(cf), FileBits(ef)
        print(of)
        print('len', len(of_bits), len(cf_bits), 'rate', len(cf_bits) / len(of_bits))
        assert of_bits == ef_bits  # origin bits == expand bits
        print()


def test_huffman():
    pass


if __name__ == '__main__':
    test_run_length()