## Introduction

This chapter covers containerization, the basics of pipelines, as well as basic ingestion.

## Docker

Docker is used to containerize applications

You can run a basic container by:
``docker run -it --rm --entrypoint=bash python:3.13.11-slim``

Where:
- `-it`: i=Interactive, t=Terminal. Allows you to interact with the application through your terminal
- `--rm`: Deletes the container after you are done with it so it isn't hanging in the background
- `--entrypoint=bash`: Enters bash so you can run bash commands. This overrides the ENTRYPOINT in the Dockerfile.
- `python:3.13.11-slim`: Docker image that we want. Pulls from the Docker image repository online.

Containers can be customized through Dockerfiles. A simple example is:

```
FROM python:3.13.11-slim

WORKDIR /code

RUN pip install uv && \
	uv init && \
	uv add pandas pyarrow

COPY pipeline/pipeline.py .

ENTRYPOINT ["uv", "run", "pipeline.py"]
```

Here:
- `FROM python:3.13.11-slim`: Every Dockerfile starts with `FROM` and uses an image, which in this case is Python 3.13.11 slim
- `WORKDIR`: This sets the working directory of the subsequent commands
- `RUN`: Runs commands in the environment's shell. Each RUN command creates a new layer. To run multiple commands in one layer, each command can be chained with `&& \` between every new line.
- `COPY`: Copies a file from a path to a specified destination
- `ENTRYPOINT`: When this container is booted up, the specified command is run(in exec format aka the first element is a command and the rest are arguments). In this case, we run "uv run pipeline.py" but each binary is enclosed in double quotes and comma separated in square brackets. 

*Note*: Entrypoint receives the arguments passed after the image name
