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
**Lempel-Ziv-Welch**数据压缩算法, 通过为连续的多个字符(字符串)分配定长的编码, 实现压缩.**LZW算法为输入中的变长模式(字符串)生成一张定长的编码编译表.**

### 压缩

* 首先为原始文件的字符集中的每个字符分配一个定长编码
* 然后从输入流中不断的为新字符串赋予更大的编码值
    1. 找出未处理的输入在符号表中最长的前缀字符串s
    2. 将s的编码值写入压缩文件
    3. 扫描s后的一个字符c
    4. 在符号表中将字符串s+c赋予下一个编码值

压缩时维护了一张以字符串作为键, 以(定长)编码为值的编译表

### 解压

* 首先, 关联编码值与字符集中的每个字符, 并用val保存解码的第一个字符
    1. 将val表示的字符(串)写入文件
    2. 从压缩文件读取一个编码x, 并得到其关联的字符串s
    3. *为val+s\[0\]分配下一个编码值*
    4. 将当前val设为s

解压时维护了一张{编码值: 字符串}的符号表

## Performance

```text
------------------------------ RunLength ------------------------------
data/4runs.bin
bits 40 -> 32 ,rate 0.800
compress 0.001s, expand 0.001s

data/abra.txt
bits 96 -> 416 ,rate 4.333
compress 0.000s, expand 0.001s

data/q32x48.bin
bits 1536 -> 1144 ,rate 0.745
compress 0.002s, expand 0.002s

data/q64x96.bin
bits 6144 -> 2296 ,rate 0.374
compress 0.008s, expand 0.006s

------------------------------ Huffman ------------------------------
data/4runs.bin
bits 40 -> 96 ,rate 2.400
compress 0.001s, expand 0.000s

data/abra.txt
bits 96 -> 120 ,rate 1.250
compress 0.001s, expand 0.001s

data/q32x48.bin
bits 1536 -> 816 ,rate 0.531
compress 0.004s, expand 0.002s

data/q64x96.bin
bits 6144 -> 2032 ,rate 0.331
compress 0.012s, expand 0.009s

data/tinytinyTale.txt
bits 408 -> 352 ,rate 0.863
compress 0.002s, expand 0.001s

data/tinyTale.txt
bits 2216 -> 1352 ,rate 0.610
compress 0.006s, expand 0.003s

data/medTale.txt
bits 45056 -> 23912 ,rate 0.531
compress 0.091s, expand 0.069s

data/tale.txt
bits 5812560 -> 3043928 ,rate 0.524
compress 11.938s, expand 7.146s

------------------------------ LZW ------------------------------
data/4runs.bin
bits 40 -> 72 ,rate 1.800
compress 0.015s, expand 0.001s

data/abra.txt
bits 96 -> 136 ,rate 1.417
compress 0.015s, expand 0.000s

data/q32x48.bin
bits 1536 -> 1176 ,rate 0.766
compress 0.025s, expand 0.003s

data/q64x96.bin
bits 6144 -> 2824 ,rate 0.460
compress 0.047s, expand 0.007s

data/tinytinyTale.txt
bits 408 -> 456 ,rate 1.118
compress 0.019s, expand 0.001s

data/tinyTale.txt
bits 2216 -> 1896 ,rate 0.856
compress 0.036s, expand 0.004s

data/medTale.txt
bits 45056 -> 27016 ,rate 0.600
compress 0.331s, expand 0.058s

data/tale.txt
bits 5812560 -> 2667936 ,rate 0.459
compress 30.548s, expand 6.579s

data/ababLZW.txt
bits 56 -> 64 ,rate 1.143
compress 0.015s, expand 0.001s

data/abraLZW.txt
bits 136 -> 160 ,rate 1.176
compress 0.015s, expand 0.001s
```

## 参考
[Algorithm fourth edition: Data compression](https://algs4.cs.princeton.edu/55compression/)