import time

import paramiko

class H3C_Switch():

    def __init__(self):
        self.HOST=''
        self.PORT=''
        self.USER=''
        self.PASSWORD=''

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

        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")
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

        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")

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
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")

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
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")
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
        print("inspect_result:" + value[len(value) - 1].strip())
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")

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
        # print(result)
        print("inspect_result:" + result)
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")

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
        print("inspect_result:" + result)
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")
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
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")

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
        print("inspect_result:" + result)
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")


class HUAWEI_Switch():
    def __init__(self):
        self.HOST=''
        self.PORT=''
        self.USER=''
        self.PASSWORD=''

    def uptime(self):
        # 创建SSH连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.HOST, port=self.PORT, username=self.USER, password=self.PASSWORD, timeout=5)
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
        print("inspect_result:" + str((int(weeks) * 7 + int(days))).strip())
        print("script_run_status:0")
        print("script_error_info:")
        print("inspect_info:")

