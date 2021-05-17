# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from config import my_sender, my_pass, my_user, smtp_server, subject

def get_msg(success_ips,faild_ips):
    Content = "======巡检结果如下=======" + '\n'
    Content += '巡检成功: ' +'\n'
    for ip in success_ips:
        Content +=  ip
        Content += '\n'
    Content += '巡检失败: ' + '\n'
    for ip in faild_ips:
        Content +=  ip
        Content += '\n'
    Content = Content + "-----------" + '\n' + "这是一份自动邮件，请不要回复！！"
    return Content

def mail(msg):
    ret = True
    try:
        MSG = MIMEText(msg, 'plain', 'utf-8')  # 填写邮件内容
        MSG['From'] = formataddr(["ZW网络检查", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        MSG['To'] = formataddr(["收件人", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        MSG['Subject'] = subject  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL(smtp_server, 465)  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(my_sender, [my_user, ], MSG.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(e)
        ret = False
    return ret


if __name__ == '__main__':
    s_ips = ['1.1.1.1','2.2.2.2']
    f_ips = ['11.11.11.11','22.22.22.22']
    msg  = get_msg(s_ips,f_ips)
    # msg = '邮件功能测试'
    ret = mail(msg)
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
