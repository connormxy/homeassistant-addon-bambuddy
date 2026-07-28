FROM ubuntu:24.04 AS build

ARG ORCA_VERSION=2.4.2
ARG TARGETARCH

# Install build dependencies and Node.js 22
RUN apt-get update && apt-get install -y \
    git curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone the repository
RUN git clone -b bambuddy/profile-resolver https://github.com/maziggy/orca-slicer-api.git .

# Download OrcaSlicer based on architecture
# AMD64: Use official AppImage from SoftFever/OrcaSlicer
# ARM64: Use custom-built AppImage from kldzj/orca-slicer-arm64
RUN if [ "$TARGETARCH" = "arm64" ]; then \
	echo "Downloading ARM64 AppImage from kldzj/orca-slicer-arm64..."; \
	curl -o orca.AppImage -L "https://github.com/kldzj/orca-slicer-arm64/releases/download/v${ORCA_VERSION}-arm64/OrcaSlicer-${ORCA_VERSION}-arm64-linux.AppImage"; \
	chmod +x orca.AppImage; \
	./orca.AppImage --appimage-extract; \
	rm orca.AppImage; \
	else \
	echo "Downloading AMD64 AppImage from OrcaSlicer/OrcaSlicer..."; \
	curl -o orca.AppImage -L "https://github.com/OrcaSlicer/OrcaSlicer/releases/download/v${ORCA_VERSION}/OrcaSlicer_Linux_AppImage_Ubuntu2404_V${ORCA_VERSION}.AppImage"; \
	chmod +x orca.AppImage; \
	./orca.AppImage --appimage-extract; \
	rm orca.AppImage; \
	fi

RUN npm ci

RUN npm run build

FROM ubuntu:24.04

# Install runtime dependencies and Node.js 22
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
	curl ca-certificates gnupg \
	libgl1 libgl1-mesa-dri libegl1 libopengl0 libglu1-mesa \
	libsm6 libice6 libmspack0 \
	libgtk-3-0 \
	libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 \
	libwebkit2gtk-4.1-0 \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
	&& update-ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

COPY --from=build /app/dist/src /app/dist
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/squashfs-root /app/squashfs-root

ENV PORT=3003
ENV ORCASLICER_PATH=/app/squashfs-root/AppRun
ENV DATA_PATH=/share/bambuddy/slicer/orca
ENV NODE_ENV=production

EXPOSE 3003

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
	CMD curl -f http://localhost:3003/health || exit 1

CMD ["node", "/app/dist/index.js"]
