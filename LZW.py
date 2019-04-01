from bitio import BitReader, BitWriter


class TST:
    """Ternary search tries, 三向单词查找树, basic function for LZW"""

    class Node:
        """树的节点"""

        def __init__(self, c, val=None, left=None, mid=None, right=None):
            self.c = c
            self.val = val
            self.left, self.mid, self.right = left, mid, right

    def __init__(self):
        self.root = None

    def get(self, key):
        """查找字符串key"""
        if not key:
            raise Exception('key must non-empty string')
        x = self._get(self.root, key, 0)
        if x is None:
            return None
        return x.val

    def _get(self, x, key, d):
        """
        递归查找
        :param x: 当前节点
        :param key: 字符串key
        :param d: 当前下标(of key)
        :return:
        """
        if x is None:
            return None
        c = key[d]
        if c < x.c:
            return self._get(x.left, key, d)
        elif c > x.c:
            return self._get(x.right, key, d)
        elif d < len(key) - 1:
            return self._get(x.mid, key, d+1)
        else:
            return x

    def put(self, key, val):
        """插入键值对 key(字符串): val"""
        if not key:
            raise Exception('key must non-empty string')
        self.root = self._put(self.root, key, val, 0)

    def _put(self, x, key, val, d):
        """
        插入键值对
        :param x: 当前节点
        :param key: 字符串key
        :param val: 值
        :param d: 当前下标(of key)
        :return:
        """
        c = key[d]
        if x is None:
            x = TST.Node(c)
        if c < x.c:
            x.left = self._put(x.left, key, val, d)
        elif c > x.c:
            x.right = self._put(x.right, key, val, d)
        elif d < len(key) - 1:
            x.mid = self._put(x.mid, key, val, d+1)
        else:
            x.val = val
        return x

    def longest_prefix_of(self, query):
        if not query:
            return None
        i, length = 0, 0
        x = self.root
        while x is not None and i < len(query):
            c = query[i]
            if c < x.c:
                x = x.left
            elif c > x.c:
                x = x.right
            else:
                i += 1
                if x.val is not None:
                    length = i
                x = x.mid
        return query[:length]


class LZW:
    """
    LZW压缩, ...
    """
    char_bit_len = 8    # 字符bit位数
    code_bit_len = 12   # 编码bit位数
    char_set_len = pow(2, char_bit_len)  # 字符集大小, 字符总数
    code_set_len = pow(2, code_bit_len)  # 编码集大小, 编码总数

    @staticmethod
    def compress(origin_filepath, compress_filepath):
        """
        将``原始文件``压缩到``压缩文件``中
        :param origin_filepath: 原始文件
        :param compress_filepath: 压缩文件
        :return: 没有返回值
        """
        st = TST()
        for i in range(LZW.char_set_len):
            st.put(chr(i), i)
        code = LZW.char_set_len + 1  # 留出char_set_len这个数字为EOF编码

        ori_f = open(origin_filepath, 'rb')
        com_f = open(compress_filepath, 'wb')

        with BitReader(ori_f) as reader:
            with BitWriter(com_f) as writer:
                # 把8位的一个字节看作一个字符作为输入(可以处理任意文件)
                input_string = []
                while True:
                    ch = reader.read_bits(LZW.char_bit_len)
                    if not reader.read:
                        break
                    input_string.append(chr(ch))
                input_string = ''.join(input_string)

                while len(input_string) > 0:
                    s = st.longest_prefix_of(input_string)  # 最长前缀
                    writer.write_bits(st.get(s), LZW.code_bit_len)  # 将s的编码写入压缩文件
                    if len(s) < len(input_string) and code < LZW.code_set_len:
                        # 将此(最长前缀+前瞻字符)构成的新子串和下一编码关联并加入符号表
                        st.put(input_string[:len(s)+1], code)
                        code += 1
                    input_string = input_string[len(s):]  # 输入中s完成读取
                writer.write_bits(LZW.char_set_len, LZW.code_bit_len)  # EOF的编码
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
        st = []
        for i in range(LZW.char_set_len):  # 用字符初始化编译表
            st.append(chr(i))
        st.append('')  # (并未使用), 看作EOF的前瞻字符

        com_f = open(compress_filepath, 'rb')
        ori_f = open(origin_filepath, 'wb')

        with BitReader(com_f) as reader:
            with BitWriter(ori_f) as writer:
                codeword = reader.read_bits(LZW.code_bit_len)
                if codeword != LZW.char_set_len:  # 文件结尾
                    val = st[codeword]
                    while True:
                        for ch in val:  # 子字符串写入
                            writer.write_bits(ord(ch), LZW.char_bit_len)
                        codeword = reader.read_bits(LZW.code_bit_len)
                        if codeword == LZW.char_set_len:
                            break
                        if len(st) == codeword:  # 需要读取的编码正是要补全符号表的条目
                            s = val + val[0]     # 这种情况下,前瞻字符必然是当前字符串首字母(好好思考下, ABABABA)
                        else:
                            s = st[codeword]  # 获取当前编码关联的字符串
                        if len(st) < LZW.code_set_len:
                            st.append(val + s[0])
                        val = s
        com_f.close()
        ori_f.close()


if __name__ == '__main__':
    # 三向单词查找树
    string = 'she sells sea shells by the sea shore'
    words = string.split()
    tst = TST()
    for idx, w in enumerate(words):
        tst.put(w, idx)
    print(tst.longest_prefix_of('shell'))

    # LZW
    src_fp = 'data/ababLZW.txt'
    com_fp = 'temp_files/ababLZW.txt.lzw'
    exp_fp = 'temp_files/ababLZW.txt'
    LZW.compress(src_fp, com_fp)
    LZW.expand(com_fp, exp_fp)
