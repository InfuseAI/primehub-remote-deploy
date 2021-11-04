#!/usr/bin/env python3
#coding: utf-8

import os
import json
from primehub import PrimeHub, PrimeHubConfig

class Config(object):
    """
    Primehub Remote Deploy Config
    """
    # Primehub Remote Deploy Config

    master_config = None
    worker_configs = []

    def __init__(self):
        self.load_sdk_config_files()
        pass

    def load_sdk_config_files(self):
        config_path = os.path.expanduser('~/.primehub/credential/')
        if self.is_phfs_exists():
            config_path = '/phfs/credential/'

        if os.path.exists(config_path) == False:
            os.makedirs(config_path)

        for f in os.listdir(config_path):
            if not f.endswith('.json'):
                continue
            name = f[:-5]
            with open(os.path.join(config_path, f)) as fd:
                config_data = json.load(fd)

            config = {
                'name': name,
                'endpoint': config_data['endpoint'],
                'path': os.path.join(config_path, f),
                'is_ready': PrimeHub(PrimeHubConfig(config=os.path.join(config_path, f))).is_ready()
            }

            if name == 'master':
                config['type'] = 'master'
                self.master_config = config
            else:
                config['type'] = 'worker'
                self.worker_configs.append(config)
        pass

    def list(self):
        """
        List all configs
        """
        result = [self.master_config] + self.worker_configs
        return [i for i in result if i]

    def set(self, name, token, endpoint, group):
        """
        Set config
        """
        config_path = os.path.expanduser('~/.primehub/credential/')
        if self.is_phfs_exists():
            config_path = '/phfs/credential/'
        sdk_config = PrimeHubConfig()
        sdk_config.set_properties(token=token, endpoint=endpoint, group=group)
        sdk_config.save(os.path.join(config_path, "%s.json" % name))
        return None

    def delete(self, name):
        """
        Delete config
        """
        isDeleted = False

        config_path = os.path.expanduser('~/.primehub/credential/')
        if self.is_phfs_exists():
            config_path = '/phfs/credential/'

        if name == 'master':
            self.master_config = None
            isDeleted = True
        else:
            for worker in self.worker_configs:
                if worker['name'] == name:
                    self.worker_configs.remove(worker)
                    isDeleted = True
                    break

        if isDeleted == True:
            os.remove(os.path.join(config_path, "%s.json" % name))
        return isDeleted

    def get(self, name):
        """
        Get config
        """
        if name == 'master':
            return self.master_config

        os.remove(os.path.join(config_path, "%s.json" % name))
        return None

    def is_phfs_exists(self):
        try:
            with open('/proc/mounts','r') as f:
                for mount in f.readlines():
                    if '/phfs' in mount:
                        return True
        except:
            pass
        return False
