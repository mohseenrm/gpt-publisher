FROM apache/airflow:2.7.1
USER root
RUN apt-get update && apt-get install -y \
    git
LABEL authors="momo"

USER airflow
WORKDIR /opt/airflow
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN pip install --upgrade pip

RUN mkdir -p gpt_publisher
WORKDIR /opt/airflow/gpt_publisher
COPY gpt_publisher/__init__.py __init__.py

WORKDIR /opt/airflow
RUN echo "Installing base package"
RUN pip install -e .
RUN echo "Installing requirements"
RUN pip install -r requirements.txt