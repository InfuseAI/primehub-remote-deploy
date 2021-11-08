#!/usr/bin/env python3
#coding: utf-8

import os
import click
from primehub import PrimeHub, PrimeHubConfig
import prettytable as pt
from .config import Config
from .deploy import Deployment

primehub_config = Config()

def is_running_in_primehub():
    return os.environ.get('JUPYTERHUB_USER') or os.environ.get('PRIMEHUB_USER')

def main():
    try:
        cli()
    except Exception as e:
        click.echo(e)

@click.group()
def cli():
    pass

@cli.group(help='Setup cluster configuration')
def config():
    pass

@config.command(name='list', help='List config')
def list_config():
    configs = primehub_config.list()

    if len(configs) == 0:
        click.echo('No configs')
        return

    table = pt.PrettyTable()
    table.field_names = ['Name', 'Type', 'Endpoint', 'Ready']
    for c in configs:
        cluster_type = 'Master' if c['name'] == 'master' else 'Worker'
        table.add_row([c['name'], cluster_type, c['endpoint'], c['is_ready']])
    print(table)
    pass

default_endpoint = 'http://primehub-graphql/api/graphql' if is_running_in_primehub() else ''

@config.command(name='set-master', help='Set master config')
@click.argument('token')
@click.option('--endpoint', prompt='Endpoint', help='Endpoint of master cluster', default=default_endpoint, show_default=True)
@click.option('--group',    prompt='Group', help='Group of master cluster', default=os.environ.get('GROUP_NAME',''), show_default=True)
def set_master_config(token, endpoint, group):
    primehub_config.set('master', token, endpoint, group)
    pass

@config.command(name='set-remote', help='Set remote config')
@click.argument('name')
@click.argument('token')
@click.option('--endpoint', prompt='Endpoint', help='Endpoint of remote cluster')
@click.option('--group',    prompt='Group', help='Group of remote cluster')
def set_remote_config(name, token, endpoint, group):
    if name == 'master':
        click.echo('Name cannot be "master"')
        exit(1)
    primehub_config.set(name, token, endpoint, group)
    pass

@config.command(name='delete', help='Delete config')
@click.argument('name')
def delete_config(name):
    if primehub_config.delete(name):
        click.echo('Config "%s" deleted' % name)
    else:
        click.echo('Config "%s" deleted' % name)
    pass

@cli.group(help='Deployment')
def deploy():
    pass

@deploy.command(name='list', help='List the deployments on master cluster')
def list_deployments():
    deploy = Deployment(primehub_config)
    deployments = deploy.list()
    table = pt.PrettyTable()
    table.field_names = ['ID', 'Name', 'Model Image', 'Status']
    for d in deployments:

        table.add_row([d['id'], d['name'], d['modelImage'], d['status']])
    print(table)
    pass

@deploy.command(name='detail', help='Show the detail information of the deployment')
@click.argument('id')
def detail_deployment(id):
    deploy = Deployment(primehub_config)
    deployment = deploy.get(id)
    deploy_table = pt.PrettyTable()
    deploy_table.title = 'Deployment: %s' % deployment['name']
    deploy_table.header = False
    deploy_table.add_row(['ID', deployment['id']])
    deploy_table.add_row(['Endpoint', deployment['endpoint']])
    deploy_table.add_row(['Access Type', deployment['endpointAccessType']])
    deploy_table.add_row(['Model Image', deployment['modelImage']])
    deploy_table.add_row(['Model URI', deployment['modelURI']])
    deploy_table.add_row(['Status', deployment['status']])
    deploy_table.add_row(['Replicas', deployment['replicas']])
    deploy_table.align = "l"
    print(deploy_table)

    if len(deployment['metadata']) > 0:
        metadata_table = pt.PrettyTable()
        metadata_table.title = 'Metadata'
        metadata_table.field_names = ['Key', 'Value']
        for k, v in deployment['metadata'].items():
            metadata_table.add_row([k, v])
        print(metadata_table)

    if len(deployment['env']) > 0:
        env_table = pt.PrettyTable()
        env_table.title = 'Environment Variables'
        env_table.field_names = ['Name', 'Value']
        for env in deployment['env']:
            env_table.add_row([env['name'], env['value']])
        print(env_table)
    pass

@deploy.command(name='sync-to-remote', help='Sync the deployment to remote cluster')
@click.argument('id', required=False)
def sync_to_remote(id=None):
    deploy = Deployment(primehub_config)
    if id != None:
        deploy.sync_to_remote(id)
    else:
        deployments = deploy.list()
        for d in deployments:
            deploy.sync_to_remote(d['id'])
    pass

if __name__ == "__main__":
    main()

