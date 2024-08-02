FROM ubuntu:24.04
ENV INDOCKER=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH
ENV DEFAULT_PYTHON=/usr/bin/python3.12

RUN apt-get update && apt-get install -y locate pipx curl gcc git python3-pip python3.12 python-apt-dev python3-dev python3-venv pkg-config

RUN mkdir /LocalCloudAgent
WORKDIR /LocalCloudAgent
RUN pipx install pipx
RUN apt-get remove -y pipx && apt-get purge
RUN pipx ensurepath --global
RUN pipx install uv
RUN echo $PATH && updatedb && locate uv && uv venv

ADD requirements* .
RUN uv pip install -r requirements-dev.txt

ADD . .
RUN chmod +x tests/docker/entry.sh

ENTRYPOINT ["/bin/bash", "-c", "./tests/docker/entry.sh"]
