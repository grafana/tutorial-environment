# Sample application for tutorials

This repository contains the environment for completing the tutorials at [grafana.com/tutorials](https://grafana.com/tutorials).

## Prequisites

You will need to have the following installed locally to complete this workshop:

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

NOTE: If you're running Docker for Desktop for macOS or Windows, Docker Compose is already included in your installation.

## Login

To log in browse to [localhost:3000](http://localhost:3000).

NOTE:
To facilitate the demo, **login has been disabled**, and anonymous access is granted admin privileges. For security reasons, we advise keeping login enabled in your Grafana instance.

If you want to follow the tutorial with login enabled, you can comment the following lines of the [docker-compose file](docker-compose.yml)


      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin 
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_BASIC_ENABLED=false


Once login is enabled, the default username and password is `admin:admin`

## Running

To start the sample application and the supporting services:

```
docker-compose up -d
```
