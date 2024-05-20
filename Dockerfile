FROM 936272581790.dkr.ecr.us-west-1.amazonaws.com/cumulonimbusinfrastructurestackecrb011c8ff-lambda8b5974b5-6kyvykzp8fdc:latest
RUN apt-get update && apt-get install -y git
ADD requirements.txt .
RUN python3 -m venv .venv
RUN .venv/bin/python -m pip install -Ur requirements.txt
ADD src .
ENTRYPOINT [".venv/bin/python", "main.py"]
