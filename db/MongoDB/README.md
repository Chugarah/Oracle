# Docker MongoDB

This repository contains a Docker Compose file that sets up a MongoDB container and a MongoDB GUI container. Follow the instructions below to activate the Docker Compose file.

## Prerequisites

Before getting started, make sure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Activation Steps

1 Edit the `.env` file and define the required environment variables:

```shell
MONGO_VERSION=6.0 
MONGO_USERNAME=admin 
MONGO_PASSWORD=secret 
HOST_PORT=27017 
CONTAINER_PORT=27017 
MONGO_GUI_PORT=8080
```

   Modify the values in the `.env` file according to your specific requirements.

2 Start the containers using Docker Compose:

```shell
# Root Directory of the Docker Compose File
cd /db/MongoDB
# Start
docker-compose up -d
# Shutdown
docker-compose down
```

3 Install GUI to Manage MongDB

Compass
Source: <https://github.com/mongodb-js/compass/?ref=retool.com>
Download: <https://github.com/mongodb-js/compass/releases>

Connect using the advanced options and paste in the username and password from the `.env` file.
for the MongoDB.
