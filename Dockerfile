FROM debian:bullseye-slim
ARG DEBIAN_FRONTEND=noninteractive

###############################################################################
# Base

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
                    eatmydata \
 && rm -rf /var/lib/apt/lists/*
###############################################################################
# DEPS

RUN eatmydata apt-get update \
 && eatmydata apt-get install -y --no-install-recommends \
                              python3-dev \
                              python3-pip \
                              python3-pytest \
                              python3-ipython \
                              git \
                              vim \
                              bash \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
###############################################################################
# CODE

COPY . /src/defeyes

RUN cd /src/defeyes \
 && pip install -r requirements-dev.txt \
 && pip install .
