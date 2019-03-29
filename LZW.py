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
    char_set_len = 256  # 字符集大小, 字符总数
    code_set_len = pow(2, code_bit_len)  # 编码集大小, 编码总数

    @staticmethod
    def compress(origin_filepath, compress_filepath):
        """
        将``原始文件``压缩到``压缩文件``中
        :param origin_filepath: 原始文件
        :param compress_filepath: 压缩文件
        :return: 没有返回值
        """
        pass

    @staticmethod
    def expand(compress_filepath, origin_filepath):
        """
        将``压缩文件``, 解压写到``原始文件``中
        :param compress_filepath: 压缩文件
        :param origin_filepath: 原始文件
        :return: 不返回任何值
        """
        pass


if __name__ == '__main__':
    # 三向单词查找树
    s = 'she sells sea shells by the sea shore'
    words = s.split()
    st = TST()
    for i, w in enumerate(words):
        st.put(w, i)
    print(st.longest_prefix_of('shell'))

    # LZW
    src_fp = 'data/tinyTale.txt'
    com_fp = 'temp_files/tinyTale.txt.lzw'
    exp_fp = 'temp_files/tinyTale.txt'
    LZW.compress(src_fp, com_fp)
    LZW.expand(com_fp, exp_fp)
