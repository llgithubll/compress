from bitstring import BitArray, ConstBitStream, Bits


class RunLength:
    """
    游程编码
    通过对重复比特计数, 实现压缩.
    """
    encoding_length = 8  # 游程长度的编码位数
    max_length = pow(2, encoding_length) - 1  # 游程的最大长度

    @staticmethod
    def expand(compress_filepath, origin_filepath):
        """
        将``压缩文件``, 解压写到``原始文件``中
        :param compress_filepath: 压缩文件
        :param origin_filepath: 原始文件
        :return: 不返回任何值
        """
        com_bits = ConstBitStream(bytes=open(compress_filepath, 'rb').read())
        com_bits_cnt = len(com_bits.bin)
        assert com_bits_cnt % RunLength.encoding_length == 0, '压缩后的bit个数必须是8的倍数'
        origin_f = open(origin_filepath, 'wb')

        ori_bits = BitArray()
        b = BitArray('0b0')
        for i in range(com_bits_cnt // 8):
            cnt = com_bits.read(8).uint
            for j in range(cnt):
                ori_bits.append(b)
            b = ~b

        ori_bits.tofile(origin_f)
        origin_f.close()

    @staticmethod
    def compress(origin_filepath, compress_filepath):
        """
        将``原始文件``压缩到``压缩文件``中
        :param origin_filepath: 原始文件
        :param compress_filepath: 压缩文件
        :return: 没有返回值
        """
        ori_bits = ConstBitStream(bytes=open(origin_filepath, 'rb').read())
        ori_bits_cnt = len(ori_bits.bin)
        compress_f = open(compress_filepath, 'wb')

        cnt = 0
        com_bits = BitArray()
        old = BitArray('0b0')
        for i in range(ori_bits_cnt):
            b = ori_bits.read(1)
            if b != old:
                com_bits.append(Bits(uint=cnt, length=RunLength.encoding_length))
                cnt = 0
                old = ~old
            else:
                if cnt == RunLength.max_length:
                    com_bits.append(Bits(uint=cnt, length=RunLength.encoding_length))
                    cnt = 0
                    com_bits.append(Bits(uint=cnt, length=RunLength.encoding_length))
            cnt += 1
        com_bits.append(Bits(uint=cnt, length=RunLength.encoding_length))

        print('compress rate:', len(com_bits.bin) / len(ori_bits.bin))
        com_bits.tofile(compress_f)
        compress_f.close()


if __name__ == '__main__':
    src_f = lambda s: 'data/' + s
    dest_f = lambda s: 'temp_files/' + s + '.rl'

    import os
    for name in os.listdir('data'):
        print(name)
        RunLength.compress(src_f(name), dest_f(name))
