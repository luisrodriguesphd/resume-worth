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

ARG MPLCONFIGDIR=".config/matplotlib"
ENV MPLCONFIGDIR=$MPLCONFIGDIR

ARG ENTRYPOINT_PATH="./entrypoint.sh"
ENV ENTRYPOINT_PATH=$ENTRYPOINT_PATH

# RUN --mount=type=secret,id=GROQ_API_KEY,mode=0444,required=true \
#     echo "GROQ_API_KEY=$(cat /run/secrets/GROQ_API_KEY)"

# Create the /code/ directory a ser permissions rwe
RUN mkdir -p /code/&& \
    chmod -R 777 /code/

# Set the working directory to /code/
WORKDIR /code

# Create a virtual environment in the directory /venv
RUN python -m venv .venv

#  Activate the virtual environment by adding it to the PATH environment variable
ENV PATH="/code/.venv/bin:$PATH"

RUN apt update && \
    python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip

COPY $REQUIREMENTS_PATH /code/requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

RUN mkdir -p $HF_HOME && \
    chmod -R 777 $HF_HOME && \
    export HF_HOME=$HF_HOME && \
    export TRANSFORMERS_CACHE=$HF_HOME && \
    mkdir -p $MPLCONFIGDIR && \
    chmod -R 777 $MPLCONFIGDIR && \
    export MPLCONFIGDIR=$MPLCONFIGDIR

COPY . .

RUN pip install -e . && \
    python src/resume_worth/pipelines/data_indexing/pipeline.py

RUN chmod +x $ENTRYPOINT_PATH

ENTRYPOINT $ENTRYPOINT_PATH
