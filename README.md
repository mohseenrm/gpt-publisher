# gpt-publisher

## Pre-requisites
- git
- docker
- docker-compose v2.21.0+

## Installation

```bash
$ pyenv virtualenv 3.11.0rc1 gpt
$ pyenv activate gpt
$ pip install -r requirements.txt
```

## Airflow webserver
```bash
$ airflow webserver --port 9000
```

### Airflow scheduler
```bash
$ airflow scheduler
```

## Docker setup

```bash
$ cp .env.example .env
$ echo -e "AIRFLOW_UID=$(id -u)" >> .env
```

```bash
$ docker-compose build
$ docker-compose up
```