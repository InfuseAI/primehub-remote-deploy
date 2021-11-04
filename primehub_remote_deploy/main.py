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
    pass

@deploy.command(name='sync-to-remote', help='Sync the deployment to remote cluster')
@click.argument('id')
def sync_to_remote(id):
    deploy = Deployment(primehub_config)
    deploy.sync_to_remote(id)
    pass

if __name__ == "__main__":
    main()

