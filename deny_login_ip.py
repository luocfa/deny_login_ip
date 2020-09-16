# -*- coding: utf-8 -*-
import re
import subprocess
import time


logFile = '/var/log/secure'
hostDeny = '/etc/hosts.deny'

# 允许的密码错误次数，大于该次数，直接拉黑
passwd_wrong_num = 1

# 获取已经加入黑名单的ip，转成字典
def getDenies():
    deniedDict = {}
    list = open(hostDeny).readlines()
    for ip in list:
        group = re.search(r'(\d+\.\d+\.\d+\.\d+)', ip)
        if group:
            deniedDict[group[1]] = '1'
    return deniedDict

# 监控方法
def monitorLog(logFile):
    # 统计密码错误次数
    tempIp = {}
    # 已拉黑ip名单
    deniedDict = getDenies()
    # 读取安全日志
    popen = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # 开始监控
    while True:
        # 1s10次吧
        time.sleep(0.1)
        # 按行读
        line = popen.stdout.readline().strip()
        if line:
            # Invalid user: 不合法的用户名的， 直接拉黑
            group = re.search(r'Invalid user \w+ from (\d+\.\d+\.\d+\.\d+)', str(line))
            # 理论上，and后面的不用判断，已经在黑名单里面的，secure日志里，直接是refused connect from XXXX
            if group and not deniedDict.get(group[1]):
                subprocess.getoutput('echo \'sshd:{}\' >> {}'.format(group[1], hostDeny))
                deniedDict[group[1]] = '1'
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print('{} --- add ip:{} to hosts.deny for invalid user'.format(time_str, group[1]))
                continue

            # 用户名合法 密码错误的
            group = re.search(r'Failed password for \w+ from (\d+\.\d+\.\d+\.\d+) ', str(line))
            if group:
                ip = group[1]
                # 统计错误次数
                if not tempIp.get(ip):
                    tempIp[ip] = 1
                else:
                    tempIp[ip] = tempIp[ip] + 1
                # 密码错误次数大于阈值的时候，直接拉黑
                if tempIp[ip] > passwd_wrong_num and not deniedDict.get(ip):
                    del tempIp[ip]
                    subprocess.getoutput('echo \'sshd:{}\' >> {}'.format(ip, hostDeny))
                    deniedDict[ip] = '1'
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    print('{} --- add ip:{} to hosts.deny for invalid password'.format(time_str, ip))

if __name__ == '__main__':
    monitorLog(logFile)
