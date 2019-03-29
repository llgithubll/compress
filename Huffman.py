import heapq
from bitio import BitReader, BitWriter


class Huffman:
    """
    Huffman压缩, 对字符(字节)统计频率, 并以此重新编码, 实现编码比特位最少
    """
    char_bit_len = 8  # 字符bit位数
    num_bit_len = 32  # 数字bit位数(用来记录文本长度)

    class Node:
        """Huffman树的节点"""
        def __init__(self, ch, freq, left=None, right=None):
            self.ch = ch
            self.freq = freq
            self.left = left
            self.right = right

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            return self.freq == other.freq

        def is_leaf(self):
            return self.left is None and self.right is None

    @staticmethod
    def _build_trie(freq):
        """
        构建Huffman单词查找树
        :param freq: 字母频率
        :return:
        """
        min_heap = []
        for ch, f in freq.items():
            heapq.heappush(min_heap, Huffman.Node(ch, f))

        while len(min_heap) > 1:
            left = heapq.heappop(min_heap)
            right = heapq.heappop(min_heap)
            parent = Huffman.Node(None, left.freq + right.freq, left, right)
            heapq.heappush(min_heap, parent)
        return heapq.heappop(min_heap)

    @staticmethod
    def _write_trie(node, writer):
        """
        将trie写入压缩文件, 解压时用
        :param node: 根节点
        :param writer: 写入组件
        :return:
        """
        if node.is_leaf():
            writer.write_bit(True)
            writer.write_bits(node.ch, Huffman.char_bit_len)
        else:
            writer.write_bit(False)
            Huffman._write_trie(node.left, writer)
            Huffman._write_trie(node.right, writer)

    @staticmethod
    def _build_code(code_table, node, s):
        """
        构建Huffman code映射表, lookup_table
        :param code_table: 编码表
        :param node: 根节点
        :param s: 字符串
        :return:
        """
        if node.is_leaf():
            code_table[node.ch] = s
        else:
            Huffman._build_code(code_table, node.left, s + '0')
            Huffman._build_code(code_table, node.right, s + '1')

    @staticmethod
    def _read_trie(reader):
        is_leaf = reader.read_bit()
        if is_leaf:
            return Huffman.Node(reader.read_bits(Huffman.char_bit_len), 0, None, None)
        else:
            return Huffman.Node(None, 0, Huffman._read_trie(reader), Huffman._read_trie(reader))

    @staticmethod
    def compress(origin_filepath, compress_filepath):
        """
        将``原始文件``压缩到``压缩文件``中
        :param origin_filepath: 原始文件
        :param compress_filepath: 压缩文件
        :return: 没有返回值
        """
        # 统计频率(一轮读取)
        freq = {}
        text_len = 0
        with open(origin_filepath, 'rb') as ori_f:
            with BitReader(ori_f) as reader:
                while True:
                    ch = reader.read_bits(Huffman.char_bit_len)
                    if not reader.read:
                        break
                    freq[ch] = freq.get(ch, 0) + 1
                    text_len += 1

        ori_f = open(origin_filepath, 'rb')
        com_f = open(compress_filepath, 'wb')

        with BitReader(ori_f) as reader:
            with BitWriter(com_f) as writer:
                root = Huffman._build_trie(freq)  # 构建Huffman树
                code_table = {}
                Huffman._build_code(code_table, root, '')  # 构建Huffman编码映射表
                Huffman._write_trie(root, writer)  # 将trie写入压缩文件, 解压时用
                writer.write_bits(text_len, Huffman.num_bit_len)  # 写入输入长度

                # 使用Huffman code编码文件(二轮读取)
                while True:
                    ch = reader.read_bits(Huffman.char_bit_len)
                    if not reader.read:
                        break
                    code = code_table[ch]
                    for b in code:
                        if b == '0':
                            writer.write_bit(False)
                        elif b == '1':
                            writer.write_bit(True)
                        else:
                            raise Exception('Illegal state')
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
                root = Huffman._read_trie(reader)
                text_len = reader.read_bits(Huffman.num_bit_len)
                for i in range(text_len):
                    x = root
                    while not x.is_leaf():
                        if reader.read_bit():
                            x = x.right
                        else:
                            x = x.left
                    writer.write_bits(x.ch, Huffman.char_bit_len)
        com_f.close()
        ori_f.close()


if __name__ == '__main__':
    src_fp = 'data/tinytinyTale.txt'
    com_fp = 'temp_files/tinytinyTale.txt.huffman'
    exp_fp = 'temp_files/tinytinyTale.txt'
    Huffman.compress(src_fp, com_fp)
    Huffman.expand(com_fp, exp_fp)
