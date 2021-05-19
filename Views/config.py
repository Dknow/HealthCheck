# -*- coding: utf-8 -*-

# 密码加密使用的salt
PASS_KEY = "woshimiyue"

# 数字签名使用的salt
TOKEN_KEY = "tokenmiyue"

# alert Email Settings
my_sender = '517422815@qq.com'  # 填写发信人的邮箱账号
my_pass = 'wrrzokvoqilkbgcd'  # 发件人邮箱授权码
my_user = '517422815@qq.com'  # 收件人邮箱账号
# smtp_server =  'smtp.163.com'
smtp_server = "smtp.qq.com"
subject = "ZW Alert"  # 邮件的主题，也可以说是标题


# username, pwd
class Config(object):
    ACCOUNT = 'admin'
    PASSWORD = 'Test1234'


    JOBS = [
        {
            'id': 'scan',  # 一个标识
            'func': 'Views.task:scan',  # 指定运行的函数
            # 'args': (1, 2),  # 传入函数的参数
            'trigger': 'interval',  # 指定 定时任务的类型
            'seconds': 60*60*24  # 运行的间隔时间,每天执行一次
        }
    ]

    SCHEDULER_API_ENABLED = True


