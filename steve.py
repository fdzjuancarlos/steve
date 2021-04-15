import argparse
import os, json
from utilities.ssh_wrapper import SSHWrapper
from strategy.maintenance import Maintenance
from strategy.deployer import Deployer

class Steve():

    def parser_init(self):
        self.parser = argparse.ArgumentParser(description='Management of production servers for angular/django webservers.')
        self.parser.add_argument("-l", "--list", help="List all servers available", action="store_true")
        self.parser.add_argument("-s", "--server", nargs=1, required=True, help="Indicates the server that must be operated")
        self.parser.add_argument("-m", "--maintenance", nargs=1, help="ON or OFF")
        self.parser.add_argument("-d", "--deploy", action="store_true", help="Activates the deploy rule for each deploy configured")
        self.args = self.parser.parse_args()
        self.server_name = self.args.server[0].strip()
        if(not self.server_name in self.servers_configs.keys()):
            raise Exception(f'No server found with given name [{self.server_name}]')
        self.active_config = self.servers_configs[self.server_name]
        self.ssh = SSHWrapper(self.servers_configs['panel'])
        self.PATH = os.path.realpath(__file__)
        self.PATH = '/'.join(self.PATH.split('/')[:-1])
        self.ASSETS_PATH = f'{self.PATH}/assets'

    def read_server_configs(self):
        self.servers_configs = {}
        path_to_json = 'servers/'
        json_files = [ ((path_to_json+pos_json), pos_json.replace('.json', '') ) for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        for pathname, server_name in json_files:
            with open(pathname) as f:
                self.servers_configs[server_name] = json.load(f)

    def __init__(self):
        self.read_server_configs()
        self.parser_init()

    def run(self, args):
        if(self.args.list):
            for key in self.servers_configs.keys():
                print(f'Server config: {key}')
        if(self.args.maintenance):
            manteinance = Maintenance(self)
            arg_lowered = self.args.maintenance[0].lower()
            if("on" in arg_lowered):
                manteinance.on()
            elif("off" in arg_lowered):
                manteinance.off()
        if(self.args.deploy):
            deployer = Deployer(self)
            deployer.start()



if __name__ == "__main__":
    steve = Steve()
    steve.run(None)