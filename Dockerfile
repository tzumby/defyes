FROM python:3.10
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
                              vim \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip \
 && pip install --no-cache-dir ipython
###############################################################################
# CODE

COPY . /src/defeyes

RUN cd /src/defeyes \
 && pip install --no-cache-dir -r requirements-dev.txt \
 && pip install --no-cache-dir .
