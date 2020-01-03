# 云服务器防止暴力密码破解

> 云服务器暴露在公网上，每天都有大量的暴力密码破解，更换端口，无济于事，该脚本监控安全日志，获取暴力破解的对方ip，加入hosts黑名单

### 路径说明
| 描述 | 路径 |
|---:|:---|
| 登录安全日志 | /var/log/secure |
| hosts黑名单 | /etc/hosts.deny |
| hosts白名单 | /etc/hosts.allow |

### 逻辑介绍
1. 通过 `subprocess.Popen('tail -f XXXXX')` 打开登录安全日志
2. `while True` 循环通过 `readline` 的形式，达到实时监控日志文件的目的
3. 解析每一行日志，出现`Invalid user \w+ from (\d+\.\d+\.\d+\.\d+)` 说明是在尝试登录不存在的用户名，那么直接拉黑当前ip
4. 出现`Failed password for \w+ from (\d+\.\d+\.\d+\.\d+)` 说明是在尝试已有用户的密码，然后判断当前ip的尝试次数，达到阈值的时候，拉黑当前ip

### 使用方法
1. 前提，准备python环境
2. 执行命令 `nohup python3 -u deny_login_ip.py >> your_log_name.log 2>&1 &`
3. 当前文件夹下会生成一个日志文件 `your_log_name.log`

### 注意事项
1. 为了防止误封自己ip的情况，请提前把自己的ip加入白名单
2. 黑白名单书写格式`sshd:172.168.0.1`， 一行一个

> 详细逻辑，见详细的代码注释

> github地址：[https://github.com/luocfa/deny_login_ip/edit/master/README.md](https://github.com/luocfa/deny_login_ip/edit/master/README.md)

