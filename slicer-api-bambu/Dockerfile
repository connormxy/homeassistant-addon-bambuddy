FROM node:24-bookworm AS build

ARG BAMBU_VERSION=02.07.01.62
ARG TARGETARCH

WORKDIR /app

# Clone the repository
RUN git clone -b bambuddy/profile-resolver https://github.com/maziggy/orca-slicer-api.git .

RUN if [ "$TARGETARCH" = "arm64" ]; then \
        echo "ARM64 not supported — BambuStudio has no official ARM64 AppImage."; \
        exit 1; \
    fi; \
    echo "Resolving BambuStudio v${BAMBU_VERSION} Ubuntu 22.04 AppImage URL..."; \
    BAMBU_URL=$(curl -fsSL "https://api.github.com/repos/bambulab/BambuStudio/releases/tags/v${BAMBU_VERSION}" \
        | grep -oE 'https://[^"]*BambuStudio_ubuntu-?22\.04[^"]*\.AppImage' \
        | head -1); \
    if [ -z "$BAMBU_URL" ]; then \
        echo "ERROR: No Ubuntu 22.04 AppImage asset found in BambuStudio v${BAMBU_VERSION}." >&2; \
        echo "Check that the release exists and ships the ubuntu-22.04 variant." >&2; \
        exit 1; \
    fi; \
    echo "Downloading $BAMBU_URL"; \
    curl -fL -o bambu.AppImage "$BAMBU_URL"; \
    chmod +x bambu.AppImage; \
    ./bambu.AppImage --appimage-extract; \
    rm bambu.AppImage

RUN npm ci
RUN npm run build

FROM node:24-bookworm-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates \
       libgl1 libgl1-mesa-dri libegl1 libopengl0 libglu1-mesa libosmesa6 \
       libsm6 libice6 libmspack0 libsoup2.4-1 \
       libgtk-3-0 \
       libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 \
       libwebkit2gtk-4.1-0 \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/dist/src /app/dist
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/squashfs-root /app/squashfs-root

ENV PORT=3001
ENV ORCASLICER_PATH=/app/squashfs-root/AppRun
ENV DATA_PATH=/share/bambuddy/slicer/bambu
ENV NODE_ENV=production
ENV BUNDLED_PROFILES_PATH=/app/squashfs-root/resources/profiles/BBL

EXPOSE 3001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3001/health || exit 1

CMD ["node", "/app/dist/index.js"]
