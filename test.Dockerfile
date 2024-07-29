FROM ubuntu:24.04
RUN apt-get update && apt-get install -y gcc git python3.12 python-apt-dev python3-dev python3-venv libgit2-dev libsystemd-dev pkg-config
RUN mkdir /LocalCloudAgent
WORKDIR LocalCloudAgent
ADD requirements* .
RUN python3.12 -m venv .venv
RUN .venv/bin/pip install -r requirements.in -r requirements-cli.in -r requirements-dev.txt
ADD . .
ENTRYPOINT [".venv/bin/tox", "-p", "all", "--parallel-live"]