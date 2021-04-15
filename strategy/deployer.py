import os
import zipfile
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

    def zipdir(self, path_to_zip, filepath_zip):
        ziph = zipfile.ZipFile(filepath_zip, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(path_to_zip):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path_to_zip, '.')))

    def deploy(self):
        deploy_configs = self.steve.active_config["deploy"]
        local_zip_filepath = "/tmp/to_upload.zip"
        server_zip_filepath = "/tmp/uploaded.zip"
        for deploy_name in deploy_configs.keys():
            path_to_backup = deploy_configs[deploy_name]['local']
            path_to_deploy = deploy_configs[deploy_name]['server']
            self.zipdir(path_to_backup, local_zip_filepath)
            self.steve.ssh.transfer_file(local_zip_filepath, server_zip_filepath)
            self.steve.ssh.rm_empty_dir(path_to_deploy)
            self.steve.ssh.execute(f'unzip {server_zip_filepath} -d {path_to_deploy}')
            self.steve.ssh.rm_file(server_zip_filepath)
            os.remove(local_zip_filepath)

    def start(self):
        self.backup()
        self.deploy()
