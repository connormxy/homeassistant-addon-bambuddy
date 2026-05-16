# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BAMBUDDY_VERSION
ARG BUILD_FROM

FROM ghcr.io/maziggy/bambuddy:${BAMBUDDY_VERSION} as builder
FROM $BUILD_FROM

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
  build-base \
  py3-opencv \
  curl \
  ffmpeg

# Install Python dependencies with cache mount
COPY --from=builder /app/requirements.txt ./
RUN sed -i 's/opencv-python-headless/# opencv-python-headless/' /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --root-user-action=ignore -r requirements.txt

COPY --from=builder /app /app

# Patch notification_service.py to support HA 2024.6 notify entities
RUN python3 -c "import re; \
path = '/app/services/notification_service.py'; \
content = open(path).read(); \
patch = '''\n\
        payload = {\n\
            \"title\": title,\n\
            \"message\": message,\n\
        }\n\
        if service and service.startswith(\"notify.\"):\n\
            payload[\"entity_id\"] = service\n\
            endpoint = \"api/services/notify/send_message\"\n\
            url = f\"{ha_url.rstrip('/')}/{endpoint}\"\n\
'''; \
content = re.sub(r'\s*payload = \{\s*\"title\": title,\s*\"message\": message,\s*\}', patch, content); \
open(path, 'w').write(content)"
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data
ENV LOG_DIR=/app/logs

# Copy root filesystem
COPY rootfs /
