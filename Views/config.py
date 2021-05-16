# -*- coding: utf-8 -*-

#密码加密使用的salt
PASS_KEY = "woshimiyue"

#数字签名使用的salt
TOKEN_KEY = "tokenmiyue"

# alert Email Settings
my_sender = '517422815@qq.com'  # 填写发信人的邮箱账号
my_pass = 'wrrzokvoqilkbgcd'  # 发件人邮箱授权码
my_user = '517422815@qq.com'  # 收件人邮箱账号
# smtp_server =  'smtp.163.com'
smtp_server =  "smtp.qq.com"
subject =  "ZW Alert" # 邮件的主题，也可以说是标题

#username, pwd
class Config(object):
    ACCOUNT = 'admin'
    PASSWORD = 'Test1234'


USER_EMAIL = 'alarm@tulong.com'
USER_SMTP ='smtp.ym.163.com'
NOTICE_SUBJECT = '途隆清洗平台邮件通知'
NOTICE_CONTENTS = '<p>这是一封系统自动发出的邮件请不要回复!<p>'