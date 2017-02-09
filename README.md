#用于从文本文件中搜索IP地址

##1、从小于1G的单个文件中搜索
+ 先将文件读取到内存中，处理速度更快，但文件过大时会导致内存溢出

> import filterIP
> IPs = filterIP.filter_ip_read("filepath")

##2、从大于1G的单个文件中搜索
+ 迭代读取，每次处理一部分，经过实测，python会自动进行buffer管理，
+ 而如果使用read(size)的方式，即使对处理过的数据进行del操作，依然会出现内存溢出的情况

>
import filterIP
IPs = filterIP.filter_ip_iter("filepath")

##3、从多个文件中批量搜索
+ 以文件为单位，多进程处理，根据文件大小自动选择合适的处理方式
+ 实测2G以内大文件的处理时间在1分钟以内，所以文件内的多线程并无太大意义

> import filterIP
> fp = filterIP.FilterIP(show=True)
> fp.start("dirpath")
> IPs = fp.IPs
> IPdict = fp.result
