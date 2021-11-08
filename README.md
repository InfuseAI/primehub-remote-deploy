# PrimeHub Remote Deploy

This repository is an example project to show how to integrate PrimeHub Python SDK to implement the remote deploy feature.
In PrimeHub, we can only deploy the [PrimeHub Deploy](https://docs.primehub.io/docs/deploy-index) to current cluster. 
If we want to deploy a model deployment to other remote clustes, we can use the command line tool `primehub-remote-deploy` to deploy.

## How to use

Please use the following container images to run the command in PrimeHub.

Image: [infuseai/primehub-remote-deploy:latest](https://hub.docker.com/repository/docker/infuseai/primehub-remote-deploy)

### Setup Cluster configs

- Add managed cluster config

  ```bash
  primehub-remote-deploy config set-master <managed-cluster-api-token>
  ```
- Add remote cluster config
  
  ```bash
  primehub-remote-deploy config set-remote <remote-cluster-name> <remote-cluster-api-token>
  ```

- List all the cluster configs
  
  ```bash
  primehub-remote-deploy config list
  ```

### List the current deployments
  ```bash
  primehub-remote-deploy deploy list
  ```

### Deploy the PrimeHub Deployment to remote clusters

  ```bash
  primehub-remote-deploy deploy sync-to-remote
  ```
