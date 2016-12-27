# -*- coding:utf-8 -*-
import os
import struct

import portalocker

class Storage(object):

    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q" # "Q" 表示无符号长整形，"!" 表示网络流的字节序，也就是大端字节序
    INTEGER_LENGTH = 8

    def __init__(self, f):
        self._f = f
        self.locked =False
        self._ensure_superblock()

    def _ensure_superblock(self):
        # 文件上锁，防止其它进程写文件
        self.lock()
        # 到达文件末尾
        self._seek_end()
        # 得到文件读取的位置（这里同时也是文件大小）
        end_address = self._f.tell()
        # 如果文件大小小于超级块大小那么必须为超级块分配足够的空间
        if end_address < self.SUPERBLOCK_SIZE:
            # 写入一串二进制零
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        # 文件解锁
        self.unlock()

    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        # 写数据大小
        self._write_integer(len(data))
        # 写数据
        self._f.write(data)
        # 返回数据块的地址
        return object_address


    def read(self, address):
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def get_root_address(self):
        # 定位到超级块的地址（也就是文件开头）
        self._seek_superblock()
        # 获取根节点地址
        root_address = self._read_integer()
        return root_address


    def commit_root_address(self, root_address):
        self.lock()
        # 刷新输出缓冲区，确认输出都已经写进硬盘
        self._f.flush()
        # 定位到超级块的地址（也就是文件开头）
        self._seek_superblock()
        # 写入根节点的地址
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def close(self):
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        return self._f.closed
