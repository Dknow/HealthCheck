import time

import paramiko

from Views.models import db, Device, Task
from Views.models import Result

from Views.Alert import MailAlert


class H3C_Switch():
    device_type = "H3C_Switch"

    def __init__(self, HOST, PORT, USER, PASSWORD, device_id):
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.device_id = device_id

    def bridge(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display interface Bridge-Aggregation brief\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            # 将接受socket输出的值
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        # 处理输出值，根据关键字截取相关内容
        value = []
        result = ""
        for line in res:
            if line.find("BAG") != -1:
                value += line.split()
        for i in range(0, len(value), 7):
            result += "Interface:" + value[0].strip() + " Link++++" + value[i + 1].strip() + "@@@@"

        print("inspect_result:" + result)
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")
        return result

    def cpuusage(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display cpu-usage\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        for line in res:
            if line.find("5 minutes") != -1:
                value += line.split()
        print("inspect_result:" + value[0].strip())

        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        return value[0].strip()

    def device(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display device\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ""
        for line in res:
            if line.find("display") == -1 and line.find(">") == -1 and line.find("Slot") == -1:
                value += line.split()
        for i in range(0, len(value), 6):
            device_name = value[i + 1]
            device_state = value[i + 2]
            result += "Name:" + device_name + " State++++" + device_state + "@@@@"
        print("inspect_result:" + result)

        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        return result

    def fan(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display fan\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            # 将接受socket输出的值
            res = ssh_shell.recv(999999).decode().split("\r\n")
        ssh.close()
        # 处理输出值，根据关键字截取相关内容
        value = []
        result = ''
        for line in res:
            if line.find("Fan") != -1 or line.find("State") != -1:
                value += line.strip("r").split(":")
        for i in range(0, len(value), 4):
            result += "Name:" + value[i].strip(":") + " State++++" + value[i + 3].strip() + "@@@@"
            # print(result)
        print("inspect_result:" + result)
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")
        return result

    def flash(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'screen-length disable\n', 'dir\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ""
        for line in res:
            if line.find("free") != -1 and line.find("total") != -1:
                value += line.split(",")
        result = ''.join(value).split()
        total = result[0].strip()
        free = result[3].strip("(").strip()
        print("inspect_result:%.2f%" % ((int(total) - int(free)) / int(total) * 100))
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        inspect_result = "%.2f%" % ((int(total) - int(free)) / int(total) * 100)
        return inspect_result

    def irf(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display irf link\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ""
        for line in res:
            if line.find("link") == -1 and line.find("Member") == -1 and line.find("Status") == -1 and line.find(
                    ">") == -1:
                value += line.split()
        for i in range(0, len(value), 3):
            result += "IRF_PORT:" + value[i] + " Statue++++" + value[i + 2] + "@@@@"
        print("inspect_result:" + result)
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        inspect_result = result
        return inspect_result

    def men(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display memory\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        for line in res:
            if line.find("Mem:") != -1 and line.find("LowMem") == -1 and line.find("HighMem") == -1:
                value += line.split()
        inspect_result = value[len(value) - 1].strip()
        print("inspect_result:" + inspect_result)
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        return inspect_result

    def ps(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display power\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(999999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ''
        for line in res:
            if line.find("display") == -1 and line.find("Slot") == -1 and line.find("PowerID") == -1 and line.find(
                    ">") == -1:
                value += line.split()
        for i in range(0, len(value), 6):
            powerid = value[i]
            state = value[i + 1]
            result = result + "powerID:" + powerid + " state++++" + state + "@@@@"
        inspect_result = result
        print("inspect_result:" + result)
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        return inspect_result

    def temperature(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display environment\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ""
        for line in res:
            if line.find("display") == -1 and line.find(">") == -1 and line.find("System") == -1 and line.find(
                    "Slot") == -1 and line.find("----") == -1:
                value += line.split()
        for i in range(0, len(value), 8):
            sensor = value[i + 1]
            temperature = value[i + 3]
            result += "Sensor:" + sensor + " temperature++++" + temperature + "@@@@"
        inspect_result = result
        print("inspect_result:" + result)
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        return inspect_result

    def uptime(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'screen-length disable\n', 'display version\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ""
        for line in res:
            if line.find("Uptime is") != -1:
                value += line.split(",")
                result = " ".join(value)
        value_list = result.split()
        days = value_list[value_list.index("days") - 1]
        weeks = value_list[value_list.index("weeks") - 1]
        print("inspect_result:" + str((int(weeks) * 7 + int(days))).strip())
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        inspect_result = str((int(weeks) * 7 + int(days))).strip()
        return inspect_result

    def s6800_ps(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display power\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(999999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ''
        for line in res:
            if line.find("display") == -1 and line.find("Slot") == -1 and line.find("PowerID") == -1 and line.find(
                    ">") == -1 and line.find("Input") == -1:
                value += line.split()
        for i in range(0, len(value), 6):
            powerid = value[i]
            state = value[i + 1]
            result = result + "powerID: " + powerid + " state++++" + state + "@@@@"
        inspect_result = result

        print("inspect_result:" + result)
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        return inspect_result

    def start(self):
        try:
            uptime = self.uptime()
            cpuusage = self.cpuusage()
            men = self.men()
            ps = self.ps()
            # result = uptime+'|'+cpuusage+'|'+men+'|'+ps
            # from Views import db
            new = result(
                device_id=self.device_id,
                cpu=cpuusage,
                uptime=uptime,
                men=men,
                ps=ps
            )
            db.session.add(new)
            db.session.flush
            print('H3C_Switch scan success:', self.device_id)
        except Exception as e:
            msg = 'H3C_Switch scan faild,device_id:{} error:{} '.format(self.device_id, str(e))
            mail(msg)


class HUAWEI_Switch():
    device_type = 'HUAWEI_Switch'

    def __init__(self, HOST, PORT, USER, PASSWORD, device_id):
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.device_id = device_id

    def uptime(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5000)
        ssh_shell = ssh.invoke_shell()
        # 将命令存在一个列表中
        cmds = ['', 'display version\n']
        for cmd in cmds:
            command = ssh_shell.sendall(cmd)
            time.sleep(1)
            res = ssh_shell.recv(9999).decode().split("\r\n")
        ssh.close()
        value = []
        result = ""
        for line in res:
            if line.find("uptime is") != -1 and line.find("Switch") == -1:
                value += line.split(",")
                result = " ".join(value)
        value_list = result.split()
        days = value_list[value_list.index("days") - 1]
        weeks = value_list[value_list.index("weeks") - 1]
        inspect_result = str((int(weeks) * 7 + int(days))).strip()
        # print("inspect_result:" + str((int(weeks) * 7 + int(days))).strip())
        # print("script_run_status:0")
        # print("script_error_info:")
        # print("inspect_info:")
        return inspect_result

    def start(self):
        try:
            uptime = self.uptime()
            new = result(
                device_id=self.device_id,
                # cpu=cpuusage,
                uptime=uptime,
                # men=men,
                # ps=ps
            )
            db.session.add(new)
            db.session.flush
            print('HUAWEI_Switch scan success:', self.device_id)
        except Exception as e:
            msg = 'HUAWEI_Switch scan faild,device_id:{} error:{} '.format(self.device_id, str(e))
            mail(msg)


linux_cmd = {"uptime": "uptime",
             "cpu": "",
             "men": "",
             "disk": "df -lh"}


class LinuxScanner():
    device_type = 'LinuxScanner'

    def __init__(self, HOST, PORT, USER, PASSWORD, device_id):
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.device_id = device_id
        self.ssh = self.get_ssh_connect()

    def get_ssh_connect(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
        except Exception as e:
            ssh = []
        return ssh

    def execc_cmd(self, cmd):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        res = ssh_stdout.read().decode()
        return res

    def version(self):
        cmd = 'cat /etc/issue'
        return self.execc_cmd(cmd)

    def uptime(self):
        cmd = 'uptime'
        return self.execc_cmd(cmd)

    # def cpu(self):
    #     cmd = 'cat /proc/stat'
    #     res =  self.execc_cmd(cmd)
    #     spl = res.split('\n')[1].split(' ')
    #     worktime = int(spl[2]) + int(spl[3]) + int(spl[4])
    #     idletime = int(spl[5])
    #     rate =  1 - float(worktime / (idletime+worktime) )
    def cpu(self):
        cmd = 'top -bn 1 -i  -c'
        res =  self.execc_cmd(cmd)
        return res
    def memory(self):
        cmd = 'free -m'
        res  =   self.execc_cmd(cmd)
        if res:
            res = res.split('\n')[1].split(' ')
            for i in res:
                if i =='':
                    res.remove(i)
        return float(int(res[2])/int(res[1]))


    def disk(self):
        cmd = linux_cmd['disk']
        res = self.execc_cmd(cmd)
        # 返回值信息太多，需要处理一下
        if res:
            res = res.split('\n')
            for i in res:
                if i.startswith('/dev/sda1'):
                    for info in i.split(' '):
                        if "%" in info:
                            res = info
                            res = float(int(res.split('%')[0]) / 100)
        return res

    def start(self):
        warnig = False
        warnig_result = []
        cpu_info = ''
        memory_info = ''
        disk_info = ''
        uptime = ''
        version = ''
        try:
            if self.ssh:
                version = self.version()
                disk_info = self.disk()
                if disk_info > 0.9:
                    warnig = True
                    warnig_result.append("DiskUsage > 90%")
                # cpu_info = self.cpu()
                # if cpu_info > 0.9:
                #     warnig = True
                #     warnig_result.append("CpuUsage Warning")
                memory_info = self.memory()
                if memory_info > 0.9:
                    warnig = True
                    warnig_result.append("MemoryUsage Warning")

                uptime = self.uptime()
            else:
                warnig = True
                warnig_result = ['无法建立ssh连接']

            if warnig:
               self.send_mail(warnig_result)
            new = Result(
                device_id=self.device_id,
                version = version,
                cpu=cpu_info,
                uptime=uptime,
                men=memory_info,
                disk=disk_info,
                ssh_connect=True if self.ssh else False

            )
            db.session.add(new)
            db.session.flush()
            print('Linux scan success:', self.device_id)

        except Exception as e:
            msg = 'Linux scan faild,device_id:{} error:{} '.format(self.device_id, str(e))
            warnig_result.append(msg)
            self.send_mail(warnig_result)
        finally:
            if self.ssh:
                self.ssh.close()

    def send_mail(self,warnig_result):
        alert = MailAlert()
        alert.send(self.device_id, self.HOST, warnig_result)

def scan():
    print('hello scan')
    # 获取配置
    tasks = Task.query.filter().all()
    D =  Device.query.filter()
    for t in tasks:
        # if t.device_type == HUAWEI_Switch.device_type:
        #     SCAN = HUAWEI_Switch(t.host, t.port, t.user, t.password, t.id)
        #     SCAN.start()
        # elif t.device_type == H3C_Switch.device_type:
        #     SCAN = H3C_Switch(t.host, t.port, t.user, t.password, t.id)
        #     SCAN.start()
        # elif t.device_type == LinuxScanner.device_type:
        #     SCAN = LinuxScanner(t.host, t.port, t.user, t.password, t.id)
        #     SCAN.start()
        d = D.filter_by(id=t.device_id).first()
        if d:
            SCAN = LinuxScanner(d.host, d.port, d.user, d.password, d.id)
            SCAN.start()


if __name__ == '__main__':
    host = "192.168.131.4"
    port = 22
    user = 'user'
    pwd = "Test1234"
    d_id = 1
    s = LinuxScanner(host, port, user, pwd, d_id)
    s.start()
