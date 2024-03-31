# See supported architectures for python image
# https://hub.docker.com/_/python
# Ex: arm64v8/python:3.11

FROM python:3.11-bookworm

LABEL maintainer="Luis Rodrigues <luisrodriguesphd@gmail.com>"
LABEL version="0.0.1"
LABEL name="ResumeWorth"
LABEL description="Discover your market value with ResumeWorth receiving a salary estimate through an advanced AI analysis"

ARG REQUIREMENTS_PATH="./requirements.in"
ENV REQUIREMENTS_PATH=$REQUIREMENTS_PATH

ARG HF_HOME=".cache/huggingface/hub"
ENV HF_HOME=$HF_HOME

ARG ENTRYPOINT_PATH="./entrypoint.sh"
ENV ENTRYPOINT_PATH=$ENTRYPOINT_PATH

# Create the /code/ directory
RUN mkdir -p /code/

# Explicitly create and set permissions for /root/llmware_data/
RUN mkdir -p /root/llmware_data/ && \
    chmod -R 777 /root/llmware_data/

# Optionally, set the umask to ensure that new files and directories
# created in /code/ have read, write, and execute permissions for everyone.
# Note: This command sets the umask for the shell used in the Dockerfile's
# RUN command, but it might not affect the umask of the shell in the running container.
# For a more persistent approach, you might need to set the umask in the container's entrypoint script.
RUN echo "umask 000" >> /etc/bash.bashrc

# Set the working directory to /code/
WORKDIR /code

# Create a virtual environment in the directory /code/venv
RUN python -m venv venv

#  Activate the virtual environment by adding it to the PATH environment variable
ENV PATH="/venv/bin:$PATH"

RUN apt update && \
    python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip

COPY $REQUIREMENTS_PATH /code/requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

RUN mkdir -p $HF_HOME && \
    chmod -R 777 $HF_HOME && \
    export TRANSFORMERS_CACHE=$HF_HOME && \
    export HF_HOME=$HF_HOME

COPY . .

RUN pip install -e . && \
    python src/resume_worth/pipelines/data_indexing/data_indexing.py && \
    chmod +x $ENTRYPOINT_PATH

ENTRYPOINT $ENTRYPOINT_PATH
