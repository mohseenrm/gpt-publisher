FROM apache/airflow:2.7.1
USER root
RUN apt-get update && apt-get install -y \
    git
LABEL authors="momo"

# Install dependencies
#COPY --from=golang:1.21.1-bookworm /usr/local/go/ /usr/local/go/
#ENV PATH="/usr/local/go/bin:${PATH}"
#RUN go version

WORKDIR /tmp
RUN curl -L https://go.dev/dl/go1.21.1.linux-amd64.tar.gz > go1.21.1.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.21.1.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/usr/local/go"
RUN go version
RUN rm -rf /tmp/go1.21.1.linux-amd64.tar.gz

RUN apt-get install hugo -y
RUN hugo version

# Install package dependencies
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