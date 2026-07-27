# Ubuntu + CUDA stuff
# Map HA's BUILD_ARCH (e.g. aarch64) to the upstream image arch (e.g. arm64) natively
ARG BUILD_ARCH=amd64
ARG ML_VERSION="1.4"

FROM thespaghettidetective/ml_api_base:${ML_VERSION}-linux-amd64 AS base-amd64
FROM thespaghettidetective/ml_api_base:${ML_VERSION}-linux-arm64 AS base-aarch64

# Select the target base image
FROM base-${BUILD_ARCH}
ARG BUILD_ARCH

########################### HA ADDON SPECIFIC PART ###########################
# Environment variables
ENV \
    CARGO_NET_GIT_FETCH_WITH_CLI=true \
    DEBIAN_FRONTEND="noninteractive" \
    HOME="/root" \
    LANG="C.UTF-8" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1 \
    PS1="$(whoami)@$(hostname):$(pwd)$ " \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    YARN_HTTP_TIMEOUT=1000000 \
    TERM="xterm-256color"

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Remove s6-overlay, bashio, and tempio installation

# Build arugments
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
ARG BUILD_REPOSITORY

# Labels
LABEL \
    io.hass.name="Obico ML" \
    io.hass.description="Home Assistant Community Add-on: Obico ML" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    io.hass.base.version=${BUILD_VERSION} \
    io.hass.base.name="obico-ml" \
    io.hass.base.image="hassioaddons/obico-ml" \
    maintainer="Connorxy" \
    org.opencontainers.image.title="Bambuddy Obico ML API" \
    org.opencontainers.image.description="Home Assistant Add-on: Bambuddy Obico ML API" \
    org.opencontainers.image.vendor="Connorxy" \
    org.opencontainers.image.authors="Connorxy" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/connormxy/homeassistant-addon-bambuddy" \
    org.opencontainers.image.source="https://github.com/connormxy/homeassistant-addon-bambuddy" \
    org.opencontainers.image.documentation="https://github.com/connormxy/homeassistant-addon-bambuddy/tree/main/obico-ml-api" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}


########################### OBICO ML API SPECIFIC PART ###########################
EXPOSE 3333

# Health check
HEALTHCHECK \
    CMD curl --fail http://0.0.0.0:3333/hc || exit 1

WORKDIR /app
ADD ./app /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN echo 'Downloading the latest failure detection AI model in Darknet format...'
RUN wget -O model/model-weights.darknet $(cat model/model-weights.darknet.url | tr -d '\r')
RUN echo 'Downloading the latest failure detection AI model in ONNX format...'
RUN wget -O model/model-weights.onnx $(cat model/model-weights.onnx.url | tr -d '\r')

# Copy entrypoint
COPY entrypoint.py /app/entrypoint.py
CMD ["python3", "/app/entrypoint.py"]