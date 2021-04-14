import paramiko

class SSHWrapper():

    def __init__(self, config):
        self.config = config
        self.ssh = None # Lazy

    def execute(self, cmd):
        if(not self.ssh):
            self.ssh = paramiko.SSHClient()
            k = paramiko.RSAKey.from_private_key_file(self.config['pkey'])
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.config['ip'], username=self.config['username'], pkey=k)

        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        print(resp)