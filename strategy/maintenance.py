

class Maintenance():

    def __init__(self, steve):
        self.steve = steve
        frontend_path = self.steve.active_config['frontend_server_path']
        self.server_path = f'{frontend_path}/maintenance.html'

    def on(self):
        maintenance_path = f'{self.steve.ASSETS_PATH}/maintenance.html'
        self.steve.ssh.transfer_file(maintenance_path, self.server_path)

    def off(self):
        self.steve.ssh.rm_file(self.server_path)