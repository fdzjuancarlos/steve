import paramiko

class SSHWrapper():

    def __init__(self, config):
        self.config = config
        self.ssh = None # Lazy

    def connect(self):
        if(not self.ssh):
            self.ssh = paramiko.SSHClient()
            k = paramiko.RSAKey.from_private_key_file(self.config['pkey'])
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.config['ip'], username=self.config['username'], pkey=k)  

    def execute(self, cmd):
        self.connect()
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        print(resp)

    def transfer_file(self, local_file, remote_path):
        self.connect()
        ftp_client = self.ssh.open_sftp()
        ftp_client.put(local_file, remote_path)
        ftp_client.close()

    def download_file(self, remote_path, local_path):
        self.connect()
        ftp_client = self.ssh.open_sftp()
        ftp_client.get(remote_path, local_path)
        ftp_client.close()

    def rm_file(self, filepath):
        self.execute( f'rm {filepath}' )