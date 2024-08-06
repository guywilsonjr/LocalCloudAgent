FROM jrei/systemd-ubuntu:latest

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
ADD tests/docker/test_startup.service /usr/lib/systemd/system/test_startup.service
RUN ln -s /usr/lib/systemd/system/test_startup.service /etc/systemd/system/multi-user.target.wants/test_startup.service
RUN chmod +x tests/docker/entry.sh
#ENTRYPOINT ["touch", "/tmp/t0/hello.txt"]
#ENTRYPOINT ["sh", "./tests/docker/entry.sh"]
ENTRYPOINT ["systemd", "start", "local_cloud_agent.service"]




