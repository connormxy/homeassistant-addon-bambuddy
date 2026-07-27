# Changelog

## [2.4.2.1] - 2026-07-27

- **Docker Containers**: Transitioned the release pipeline to use GitHub Actions and GHCR using Home Assistant's newest guidance for Docker builds. The add-on is now distributed as a pre-built Docker image, reducing local installation time and storage requirements.
- **Source Build**: Transitioned the build pipeline to compile natively from the upstream source repository, ensuring better long-term reliability and flexibility.
- **Debian Migration**: Moved base image to Debian Bookworm to natively resolve `libwebkit2gtk-4.1-0` dependencies.

## 2.3.2.2
- Added native healthchecks to accurately reflect container startup state


All notable changes to the App will be documented in this file.

## [2.3.2.1] - 2026-06-10
- **Pre-compiled Images**: The add-on now pulls directly from the pre-built `ghcr.io/maziggy/orca-slicer-api` image instead of compiling from source. This eliminates build failures on platforms lacking Git/BuildKit and dramatically speeds up installation.

## [2.3.2] - 2026-06-09
- **Upstream Sync**: Adopted consistent versioning scheme matching the underlying OrcaSlicer version (`2.3.2`).

## [1.1] - 2026-05-15
- Initial stable release of the dedicated Slicer API sidecar container.
