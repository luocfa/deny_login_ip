# deny_login_ip

> 云服务器暴露在公网上，每天都有大量的暴力密码破解，更换端口，无济于事，该脚本监控安全日志，获取暴力破解的对方ip，加入hosts黑名单

| 描述 | 路径 |
|---:|:---|
| 安全日志路径 | /var/log/secure |
| hosts黑名单 | /etc/hosts.deny |

### 使用方法

1. 前提，准备python环境
2. 执行命令 `nohup python3 -u deny_login_ip.py >> your_log_name.log 2>&1 &`
3. 当前文件夹下会生成一个日志文件 `your_log_name.log`

> 详细逻辑，见详细的代码注释

> thank you for your star!
