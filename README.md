# sedmail.zabbix.py
关于Zabbix6.0.2发送带截图邮箱报警的脚本
# 环境
Zabbix6.0.2（5.0或以下版本可能不行）
Python3
# 内容
## 脚本存放
主要脚本为`sedmail.zabbix.sh`和`sedmail.zabbix.py`，请都放在`/usr/lib/zabbix/alertscripts/`目录下
* `sedmail.zabbix.sh`为shell脚本，用于连接python（Zabbix6.0版本貌似不能直接调用python脚本）、debug和删除图片
* `sedmail.zabbix.py`为python3脚本，负责下载图片、发送邮件
## 脚本参数修改
`sedmail.zabbix.py`内的user、password、host、smtp_host、from_email、mail_pass记得修改
| 参数          | 作用                               | 例子                          |备注                          |
|---------------|------------------------------------|-------------------------------|-------------------------------|
| `user`        | 定义 Zabbix 用户名                 | `user='Admin'`               ||
| `password`    | 定义 Zabbix 用户密码               | `password='Zabbix后台密码'`   ||
| `graph_path`  | 定义图片存储路径                  | `graph_path='/usr/lib/zabbix/alertscripts/graph'` ||
| `host`        | 定义主机 IP 地址                   | `host='192.168.32.241'`      ||
| `graph_url`   | 定义图表的 URL                     | `graph_url=f'http://{host}:8080/chart.php'` |这里一般要修改端口号和http或https|
| `login_url`   | 定义登录的 URL                    | `login_url=f'http://{host}:8080/index.php'` |这里一般要修改端口号和http或https|
| `smtp_host`   | 定义 SMTP 服务器地址              | `smtp_host='smtp.xx.com'`    |这里默认使用加密的smtp|
| `from_email`  | 定义发件人地址                    | `from_email='alittlemc@foxmail.com'` ||
| `mail_pass`   | 发件人邮箱校验码                  | `mail_pass='你的邮箱密码'`     ||
  
## 图片临时存放
建议在脚本目录下新建一个`graph`文件夹并chmod读写权限，即`/usr/lib/zabbix/alertscripts/graph`用于存放文件


# 详细教程请见
[服务器-Zabbix6.0使用Python脚本实现带图片的邮箱的报警](https://www.cnblogs.com/alittlemc/p/17984208)

![效果图](https://img2024.cnblogs.com/blog/2928139/202401/2928139-20240124111257910-1882055126.png)

