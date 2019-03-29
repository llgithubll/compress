# 数据压缩

## First...

[python二进制文件的读写操作](https://rosettacode.org/wiki/Bitwise_IO#Python)


## 游程编码
比特流中最简单的冗余形式就是一长串重复的比特. 游程编码对这些重复比特计数, 交替保存0和1的长度, 实现"压缩".
适合大量重复长游程的情况, 不适合大量短游程的数据(比如自然语言文档)

### 压缩
* 读取一个比特
* 如果它和上一个比特不同, 写入当前的计数值并将计数器归零
* 如果它和上一个比特相同且计数器已达到最大值, 则写入计数值, 再写入一个0计数值, 然后将计数值归零
* 增加计数器的值

输入流结束时, 写入计数值(最后一个游程长度)并结束.

### 解压
读取一个游程的长度, 将当前比特按照长度写入解压文件, 转换当前比特然后继续, 直到输入结束

## Huffman
Huffman压缩, 通过对字符统计频率, 为频率高的构建短编码, 为频率低的构建长编码, 使得总体编码长度最小.
非常适用于自然语言文本(对其他任意字节流也有效果), **Huffman算法为输入中的定长模式产生了一张变长的编码编译表.**

### 压缩
(将需要压缩的比特流看作8位编码的字符值, 然后按以下方式压缩)
* 读取输入
* 统计输入中的每个字符值出现的频率
* 根据频率构建Huffman树
* 根据Huffman树构建每个字符的Huffman编码的编译表
* 将单词查找树(Huffman树)编码为比特流写入压缩文件
* 将字符总数编码写入压缩文件
* 使用编译表编码每个输入字符, 并写入压缩文件

### 解压
* 读取单词查找树(Huffman树,在压缩文件开头)
* 读取需要解码的字符数量
* 使用单词查找树(Huffman树)对后续比特流解码




## LZW
**Lempel-Ziv-Welch**数据压缩算法, 通过为连续的多个字符(字符串)分配定长的编码, 实现压缩.

**LZW算法为输入中的变长模式生成一张定长的编码编译表.**



## 参考
[Algorithm fourth edition: Data compression](https://algs4.cs.princeton.edu/55compression/)