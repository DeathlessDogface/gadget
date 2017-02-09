#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
下载指定的http或ftp文件
@author:jiaoshijie
@date:2016.11.23
"""
from os import path, mkdir
from re import compile
from urllib2 import urlopen
from urlparse import urlparse


class DownLoad(object):
    def __init__(self):
        super(DownLoad, self).__init__()
        self.re_true = compile(r'[^\s]')

    def download(self, address):
        """
        下载文件
        :param address: 下载地址
        :return: 真实地址、页面文本
        """
        if not address.startswith('http') and not address.startswith('ftp'):
            address = "http://" + address
        page = urlopen(address)
        url = page.url
        content = page.readlines()
        first = last = ""
        for line in content:
            if self.re_true.findall(line):
                if not first:
                    first = line
                last = line
        info = first[:70] + "..." + last[-10:]
        page.close()
        return url, info, ''.join(content)

    def downsave(self, address, store):
        """
        下载文件并保存在本地
        :param address: 下载地址
        :param store:  存储目录
        """
        url, info, page = self.download(address)
        parser = tuple(urlparse(url))
        pathlist = [store, parser[1]] + parser[2].split('/')
        pathlist = [x for x in pathlist if x]
        pathlist = map(lambda x: x.replace('/', path.sep), pathlist)
        dirpath = path.join(*pathlist[:-1])
        filename = pathlist[-1]
        if "." not in filename:
            filename = filename + ".txt"
        self.makedirs(dirpath)
        with open(path.join(dirpath, filename), 'w') as f:
            f.write(page)
        return url, info

    def makedirs(self, dirpath):
        if not path.isdir(dirpath):
            fatherpath, name = path.split(dirpath)
            if path.isdir(fatherpath):
                mkdir(dirpath)
            else:
                self.makedirs(fatherpath)
                mkdir(dirpath)


DownLoad = DownLoad()

if __name__ == "__main__":
    page = DownLoad.downsave('http://10.10.2.243/dvwa/vulnerabilities/', 'D:/cookbook/test/')
    print page[:2]
