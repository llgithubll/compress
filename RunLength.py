from bitio import BitReader, BitWriter


class RunLength:
    """
    游程编码: 通过对重复比特计数, 实现压缩.
    """
    encoding_length = 8  # 游程长度的编码位数
    max_length = pow(2, encoding_length) - 1  # 游程的最大长度

    @staticmethod
    def compress(origin_filepath, compress_filepath):
        """
        将``原始文件``压缩到``压缩文件``中
        :param origin_filepath: 原始文件
        :param compress_filepath: 压缩文件
        :return: 没有返回值
        """
        ori_f = open(origin_filepath, 'rb')
        com_f = open(compress_filepath, 'wb')

        with BitReader(ori_f) as reader:
            with BitWriter(com_f) as writer:
                cnt = 0
                old = False
                while True:
                    b = True if reader.read_bit() else False
                    if not reader.read:  # End-of-file?
                        break
                    if b is not old:
                        writer.write_bits(cnt, RunLength.encoding_length)
                        cnt = 0
                        old = not old
                    else:
                        if cnt == RunLength.max_length:
                            writer.write_bits(cnt, RunLength.encoding_length)
                            cnt = 0  # 另一种比特长度为0, 然后可以接着继续之前的比特计数
                            writer.write_bits(cnt, RunLength.encoding_length)
                    cnt += 1
                writer.write_bits(cnt, RunLength.encoding_length)

        ori_f.close()
        com_f.close()

    @staticmethod
    def expand(compress_filepath, origin_filepath):
        """
        将``压缩文件``, 解压写到``原始文件``中
        :param compress_filepath: 压缩文件
        :param origin_filepath: 原始文件
        :return: 不返回任何值
        """
        com_f = open(compress_filepath, 'rb')
        ori_f = open(origin_filepath, 'wb')
        with BitReader(com_f) as reader:
            with BitWriter(ori_f) as writer:
                b = False
                while True:
                    cnt = reader.read_bits(RunLength.encoding_length)
                    if not reader.read:  # End-of-file?
                        break
                    for i in range(cnt):
                        writer.write_bit(b)
                    b = not b
        com_f.close()
        ori_f.close()


if __name__ == '__main__':
    src_fp = 'data/4runs.bin'
    com_fp = 'temp_files/4runs.bin.rl'
    exp_fp = 'temp_files/4runs.bin'
    RunLength.compress(src_fp, com_fp)
    RunLength.expand(com_fp, exp_fp)
