#!/usr/bin/python3
#coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib,sys,os,time,re,requests,logging
from smtplib import SMTP

# 请按照实际情况修改参数
user='Admin'    #定义zabbix用户名
password='Zabbix后台密码'    #定义zabbix用户密码
graph_path='/usr/lib/zabbix/alertscripts/graph'   #定义图片存储路径
host='192.168.32.241'
graph_url = f'http://{host}:8080/chart.php' #定义图表的url，这里修改你的端口号、http或https
login_url = f'http://{host}:8080/index.php' #定义登录的url，这里修改你的端口号、http或https
to_email=sys.argv[1]    #传入的第一个参数为收件人邮箱
subject=sys.argv[2]  #传入的第二个参数为邮件主题
subject=subject.encode('utf-8').decode('utf-8')
smtp_host = 'smtp.xx.com'  #定义smtp服务器地址
from_email = '你的邮箱@xx.com'     #定义发件人地址
mail_pass = '你的邮箱密码'       #发件人邮箱校验码

def get_itemid():
    #获取报警的itemid
    itemid=re.search(r'监控ID:(\d+)',sys.argv[3]).group(1) # 如果修改了Zabbix文字模版，这里对应的也需要修改
    return itemid

def get_graph(itemid):
    #获取报警的图表并保存
    session=requests.Session()   #创建一个session会话
    try:
        loginheaders={
        "Host":host,
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
        #定义请求消息头

        payload = {
        "name":user,
        "password":password,
        "autologin":"1",
        "enter":"登录",
        }
        #定义传入的data
        login=session.post(url=login_url,headers=loginheaders,data=payload)
        # print(login.text)
        #进行登录
        graph_params={
            "from" :"now-30m",  # 这里可以修改图片的时间轴，30m即最30分钟
            "to" : "now",
            "itemids[0]" : itemid,
            "width" : "300",    #宽度
        }
        # print(itemid)
        # http://zabbix:8080/chart.php?from=now-1m&to=now&itemids%5B0%5D=79672

        #定义获取图片的参数
        graph_req=session.get(url=graph_url,params=graph_params,headers=loginheaders)
        #发送get请求获取图片数据
        time_tag=time.strftime("%Y%m%d%H%M%S", time.localtime())
        graph_name='baojing_'+time_tag+'.png'
        #用报警时间来作为图片名进行保存
        graph_name = os.path.join(graph_path, graph_name)
        #使用绝对路径保存图片
        with open(graph_name,'wb') as f:
            f.write(graph_req.content)
            #将获取到的图片数据写入到文件中去
        return graph_name

    except Exception as e:
        # print(e)
        return False
def text_to_html(text):
    #将邮件内容text字段转换成HTML格式
    d=text.splitlines()
    #将邮件内容以每行作为一个列表元素存储在列表中
    html_text=''
    for i in d:
        i='' + i + '<br>'
        html_text+=i + '\n'
    #为列表的每个元素后加上html的换行标签
    return html_text

def send_mail(graph_name):
    #将html和图片封装成邮件进行发送
    msg = MIMEMultipart('related')  #创建内嵌资源的实例

    with open(graph_name,'rb') as f:
        #读取图片文件
        graph=MIMEImage(f.read())  #读取图片赋值一个图片对象
    graph.add_header('Content-ID','imgid1')  #为图片对象添加标题字段和值
    text=text_to_html(sys.argv[3])
    html="""
    <html>
      <body>
      %s  <br><img src="cid:imgid1">
      </body>
    </html>
    """ % text
    html=MIMEText(html,'html','utf-8')  #创建HTML格式的邮件体
    msg.attach(html)   #使用attach方法将HTML添加到msg实例中
    msg.attach(graph)  #使用attach方法将图片添加到msg实例中
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        server=SMTP(smtp_host,"587")   #创建一个smtp对象
        server.starttls()    #启用安全传输模式
        server.login(from_email,mail_pass)  #邮箱账号登录
        server.sendmail(from_email,to_email.split(','),msg.as_string())  #发送邮件
        server.quit()   #断开smtp连接
    except smtplib.SMTPException as a:
        print(a)

def run():
    itemid=get_itemid()
    graph_name=get_graph(itemid)
    send_mail(graph_name)

if __name__ =='__main__':
    run()
    print('success',sys.argv[1],sys.argv[2],sys.argv[3])
