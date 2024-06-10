ARG VERSION
FROM 936272581790.dkr.ecr.us-west-1.amazonaws.com/cumulonimbusinfrastructurestackecrb011c8ff-pythona57b7ce0-zwlwp6r36elt
ARG VERSION
ENV VERSION=$VERSION
RUN apt-get update && apt-get install -y git
ADD requirements.txt .
RUN python3 -m venv .venv
RUN git config --global --add safe.directory '*'
RUN .venv/bin/python -m pip install -Ur requirements.txt
ADD src/local_cloud_agent .
RUN git config --global --add safe.directory '*'
ENTRYPOINT [".venv/bin/python", "main.py"]
