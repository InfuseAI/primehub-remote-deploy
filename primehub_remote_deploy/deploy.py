#!/usr/bin/env python3
#coding: utf-8

import os
import json
from primehub import PrimeHub, PrimeHubConfig

class Deployment(object):
    primehub_config = None
    ph = None
    def __init__(self, config):
        self.primehub_config = config
        if self.primehub_config.master_config == None:
            raise Exception("No master config found")
        self.master = PrimeHub(
            PrimeHubConfig(config=self.primehub_config.master_config.get('path'))
        )

    def list(self):
        return self.master.deployments.list()

    def get(self, id):
        return self.master.deployments.get(id)

    def sync_instancetype_to_worker(self, name, ph_worker):
        instancetype = self.master.admin.instancetypes.get(name)
        del instancetype['id']

        if ph_worker.admin.instancetypes.get(name) == None:
            ph_worker.admin.instancetypes.create(instancetype)
            print("Created instance type: {}".format(name))
        else:
            print("Found instance type: {}".format(name))

    def sync_deployment_to_worker(self, deployment, ph_worker):
        isNewCreated = False
        try:
            ph_worker.deployments.get(deployment['id'])
            print("Updatomg deployment: {}".format(deployment['id']))
        except:
            print("Creating deployment: {}".format(deployment['id']))
            isNewCreated = True

        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(deployment)

        if isNewCreated:
            create_deployment_config = {
                'id': deployment['id'],
                'name': deployment['name'],
                'description': deployment['description'] or "",
                'instanceType': deployment['instanceType']['name'],
                'modelImage': deployment['modelImage'],
                'modelURI': deployment['modelURI'],
                'replicas': deployment['replicas'],
                'imagePullSecret': deployment['imagePullSecret'] or "",
                'endpointAccessType' : deployment['endpointAccessType'],
                'updateMessage': deployment['updateMessage'],
            }
            ph_worker.deployments.create(create_deployment_config)
        else:
            update_deployment_config = {
                'description': deployment['description'] or "",
                'instanceType': deployment['instanceType']['name'],
                'modelImage': deployment['modelImage'],
                'modelURI': deployment['modelURI'],
                'replicas': deployment['replicas'],
                'imagePullSecret': deployment['imagePullSecret'] or "",
                'endpointAccessType' : deployment['endpointAccessType'],
                'updateMessage': deployment['updateMessage']
            }
            ph_worker.deployments.update(deployment['id'], update_deployment_config)
        if deployment['status'] == 'Stopped':
            ph_worker.deployments.stop(deployment['id'])
        elif deployment['status'] == 'Deployed':
            ph_worker.deployments.start(deployment['id'])
        print('[Done]')

    def sync_to_remote(self, id):
        deployment = self.get(id)
        for worker in self.primehub_config.worker_configs:
            print('[Sync] Worker: {}'.format(worker['name']))
            ph_worker = PrimeHub(
                PrimeHubConfig(config=worker.get('path'))
            )
            instancetype = deployment['instanceType']['name']
            self.sync_instancetype_to_worker(instancetype, ph_worker)
            self.sync_deployment_to_worker(deployment, ph_worker)

