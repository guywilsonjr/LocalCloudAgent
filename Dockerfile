FROM 936272581790.dkr.ecr.us-west-1.amazonaws.com/cumulonimbusinfrastructurestackecrb011c8ff-pythona57b7ce0-zwlwp6r36elt:latest
RUN apt-get update && apt-get install -y git
ADD requirements.txt .
RUN python3 -m venv .venv
RUN .venv/bin/python -m pip install -Ur requirements.txt
ADD src .
ENTRYPOINT [".venv/bin/python", "main.py"]
