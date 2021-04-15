import os
from datetime import datetime

class Deployer():

    def make_dirs(self):
        os.makedirs(self.backup_localdir, exist_ok=True)

    def __init__(self, steve):
        self.steve = steve
        self.backup_filepath = "/tmp/backup.zip"
        self.backup_localdir = self.steve.PATH + '/backups/' + self.steve.server_name
        now = datetime.now()
        strftime = now.strftime("%Y-%m-%d-%H-%M-%S")
        self.local_backup_filepath = self.backup_localdir + f'/{strftime}.zip' 
        self.make_dirs()

    def backup(self):
        deploy_configs = self.steve.active_config["deploy"]
        paths_to_backup = ''
        for deploy_name in deploy_configs.keys():
            paths_to_backup += deploy_configs[deploy_name]['server'] + ' '
        if paths_to_backup:
            self.steve.ssh.execute(f'zip -r {self.backup_filepath} {paths_to_backup}')
            self.steve.ssh.download_file(self.backup_filepath, self.local_backup_filepath)
            self.steve.ssh.rm_file(self.backup_filepath)
        else:
            raise Exception("No paths to backup detected")

    def deploy(self):


    def deploy(self):
        self.backup()
