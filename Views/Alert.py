# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from Views import db
from Views.config import my_sender, my_pass, my_user, smtp_server, subject
from Views.models import EmailHistory


class MailAlert():

    def format_msg(self, device_id, ip, warning_result):
        msg = "HealthCheck Warning Alert" + '\n'
        msg += "设备id：" + str(device_id) + "  " + "设备ip：" + ip + "\n"
        msg += "Warning Reason:" + '   '.join(warning_result) +'\n'
        return msg

    def mail(self,msg):
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

    def send(self, device_id, ip, warning_result):
        msg = self.format_msg(device_id, ip, warning_result)
        self.mail(msg)
        self.add_mail_record(device_id,warning_result)

    def add_mail_record(self,device_id,warning_result):
        new  = EmailHistory(
            device_id = device_id,
            warning=True if warning_result else False,
            warning_result = str(warning_result),
            recive_email =  my_user
        )
        db.session.add(new)
        db.session.flush()



if __name__ == '__main__':
    msg = '邮件功能测试'
    ret = mail(msg)
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
