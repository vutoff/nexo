# Simple python web application

## Requirements
- Python ~> 3.7
- Docker
- Kubernetes cluster running locally (tested on [Rancher Desktop](https://rancherdesktop.io/))
- Helm

## Automated Docker image build and push to the registry

The CI relies on GitHub Actions to build and push a docker image. The said image is tagged with the commit SHA.
The pipeline requires two secrets to be set at the repo Secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` - can be obtained from Docker HUB: Account Settings -> Security -> New Access Token

## Deploy to local K8s cluster
### Pre-requisites
- Edit `values.image.repository` and set the correct image name (and optionally repo if not hosted in DockerHub)
- Make sure the image is already built and pushed to the said registry
- Make sure that `appVersion` set in `nexo/Chart.yml` corresponds to the Docker image tag you're about to deploy.


### Deploy
```sh
$ helm install nexo nexo --values nexo/values.yaml
```

The service is configured with NodePort. Run the following commands to get the correct URL for verification:

```sh
export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services nexo)
export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
echo http://$NODE_IP:$NODE_PORT
```

## Testing locally

### Start local MySQL server

```sh
docker run -d --name mysql -e MYSQL_ROOT_PASSWORD='test' mysql:8.0.30
```

### Start the application server

```sh
$ python -m pip install -r app/requirements.txt
$ export MYSQL_USER='root'
$ export MYSQL_PASSWORD='test'
$ export MYSQL_HOST='mysql'
$ python app/app.py
    * Serving Flask app 'app' (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Running on all addresses (0.0.0.0)
    WARNING: This is a development server. Do not use it in a production deployment.
    * Running on http://127.0.0.1:8181
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 330-062-796
```

then navigate to http://127.0.0.1:8181 via web browser

### Test using docker-compose

```sh
$ IMAGE_TAG="0.1" docker-compose up -d
```

This will build an image with tag set by `IMAGE_TAG` and run a docker container locally from it
