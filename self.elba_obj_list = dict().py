  self.elba_obj_list = dict()
        self.switch_obj_list = dict()
        for item in self.script_params['dss_list']:
            for i in item:
                a = CXOsCli(
                    self.topology_dict['DEVICES'][i]['mgmt_ip'],
                    self.topology_dict['DEVICES'][i]['username'],
                    # key_file=os.path.join(os.path.abspath(os.getcwd()), 'config', 'Taormina', 'login.pem')
                    ssh_password=self.topology_dict['DEVICES'][i]['password']
                )
                self.switch_obj_list[i] = a
        for item in self.script_params['dss_list']:
            for elba in self.input_dict['elba_map']:
                for i in item:
                    a = CXOsCli(
                        self.topology_dict['DEVICES'][i]['mgmt_ip'],
                        self.topology_dict['DEVICES'][i]['username'],
                        # key_file=os.path.join(os.path.abspath(os.getcwd()), 'config', 'Taormina', 'login.pem')
                        ssh_password=self.topology_dict['DEVICES'][i]['password']
                    )
                    key = i + "-" + elba
                    self.elba_obj_list[key] = a