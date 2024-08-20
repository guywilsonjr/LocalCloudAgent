FROM jrei/systemd-ubuntu:latest AS base

ENV PYTHONUNBUFFERED=1


FROM base AS init


RUN apt-get update && apt-get install -y  \
    locate  \
    pipx  \
    curl  \
    gcc  \
    git  \
    python3-pip  \
    python3.12  \
    python-apt-dev  \
    python3-dev  \
    python3-venv  \
    pkg-config \
    vim

RUN mkdir /LocalCloudAgent
ADD requirements* /LocalCloudAgent/

FROM init AS setup
ENV PATH=/root/.local/bin:$PATH
ENV VIRTUAL_ENV=/LocalCloudAgent/.venv

WORKDIR /LocalCloudAgent

RUN python3.12 -m venv .venv && .venv/bin/pip install -U pip setuptools
RUN .venv/bin/pip install uv
RUN .venv/bin/pip install tox-uv
RUN .venv/bin/uv pip install -r requirements.txt

ADD tests/docker/test_startup.service /usr/lib/systemd/system/test_startup.service
RUN ln -s /usr/lib/systemd/system/test_startup.service /etc/systemd/system/multi-user.target.wants/test_startup.service


FROM setup AS install
ENV VIRTUAL_ENV=/LocalCloudAgent/.venv

ADD . .
RUN chmod +x tests/docker/entry.sh


FROM install AS final
ENV INDOCKER=1
ENV PYTHONPATH=/LocalCloudAgent/src
WORKDIR /
ENTRYPOINT ["systemd", "start", "test_startup.service"]




