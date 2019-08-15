#!/usr/bin/python
# coding=utf-8

import datetime
import json
import os
import re
import threading
import time

import chardet
import nmap
import requests

requests.packages.urllib3.disable_warnings()
try:
    # python3 为小写
    import queue
except ImportError:
    # python2 为大写
    import Queue

# 存放输出内容
final_domains = []
# 定义一个引用外部全局对象
gl = globals()


# 线程的一种实现方式 (重写)
class PortScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while not self._queue.empty():
            scan_ip = self._queue.get()
            try:
                portScan(scan_ip)
                nmapScan(scan_ip)
            except Exception as e:
                print(e)
                pass


# 调用masscan
def portScan(scan_ip):
    print('portScan-------------- 多线程处理 -------------------- ' + scan_ip);
    temp_ports = []  # 设定一个临时端口列表
    os.system('masscan/bin/masscan ' + scan_ip + ' -p 1-65535 -oJ output/' + scan_ip + '.json --rate 500')
    print('当前ip 输出文件------------------------------------ ' + scan_ip)
    # 提取json文件中的端口
    for line in open('output/' + scan_ip + '.json', 'r'):
        if line.startswith('{ '):
            temp = json.loads(line[:-1])
            temp1 = temp["ports"][0]
            temp_ports.append(str(temp1["port"]))
    if len(temp_ports) > 50:
        temp_ports.clear()  # 如果端口数量大于50，说明可能存在防火墙，属于误报，清空列表
    else:
        # 赋值端口列表到 当前 ip 变量名为当前ip
        gl['ip' + ''.join(scan_ip.split('.'))] = temp_ports  # 小于50则放到总端口列表里


# 调用nmap识别服务
def nmapScan(scan_ip):
    nm = nmap.PortScanner()
    try:
        # 获取端口列表 列表名称为当前 ip
        for port in eval('ip' + ''.join(scan_ip.split('.'))):
            # -sS 需要root权限,TCP SYN 的方式来对目标主机进行扫描
            # -Pn #跳过主机发现,进行直接进行更深层次的扫描
            ret = nm.scan(scan_ip, port, arguments='-Pn,-sS,-sV,-A')
            service_name = ret['scan'][scan_ip]['tcp'][int(port)]['name']
            print(' 主机' + scan_ip + '    端口  ' + str(port) + '    服务名为  ' + service_name)
            if 'http' in service_name or service_name == 'sun-answerbook':
                if service_name == 'https' or service_name == 'https-alt':
                    scan_url_port = 'https://' + scan_ip + ':' + str(port)
                    webTitle(scan_url_port, service_name)
                else:
                    scan_url_port = 'http://' + scan_ip + ':' + str(port)
                    webTitle(scan_url_port, service_name)
            else:
                final_domains.append(scan_ip + ':' + str(port) + '      ' + service_name)
    except Exception as e:
        print(e)
        pass


# 获取网站的web应用程序名和网站标题信息
def webTitle(scan_url_port, service_name):
    try:
        r = requests.get(scan_url_port, timeout=3, verify=False)
        # 获取网站的页面编码
        r_detectencode = chardet.detect(r.content)
        actual_encode = r_detectencode['encoding']
        response = re.findall(u'<title>(.*?)</title>', r.content, re.S)
        if response == []:
            final_domains.append(scan_url_port + '      ' + service_name)
        else:
            # 将页面解码为utf-8，获取中文标题
            res = response[0].decode(actual_encode).decode('utf-8')
            banner = r.headers['server']
            final_domains.append(scan_url_port + '      ' + banner + '      ' + res)
    except Exception as e:
        print(e)
        pass


# 启用多线程扫描
def main():
    queue = Queue.Queue()
    count = 0
    try:
        for count, line in enumerate(open('ip.txt', 'r')):
            if '\n' in line:
                final_ip = line.strip()
            if '\r' in line:
                final_ip = line.strip()
            if '\r' not in line and '\n' not in line:
                final_ip = line
            queue.put(final_ip)
            count += 1
        threads = []
        thread_count = count
        for i in range(thread_count):
            threads.append(PortScan(queue))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    tmp_domians = []
    ff = open(r'output_result_' + str(time.time()).split('.')[0] + '.txt', 'w')
    for tmp_domain in final_domains:
        if tmp_domain not in tmp_domians:
            ff.write(tmp_domain + '\n')
    ff.close()
    spend_time = (datetime.datetime.now() - start_time).seconds
    print('程序共运行了： ' + str(spend_time) + '秒')
