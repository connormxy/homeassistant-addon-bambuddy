# Changelog

## [02.07.01.62.2] - 2026-07-27

- **Fix**: Fixed HAOS 404 installation errors by explicitly linking the new multi-arch image names.
- **Docker Containers**: Transitioned the release pipeline to use GitHub Actions and GHCR using Home Assistant's newest guidance for Docker builds. The add-on is now distributed as a pre-built Docker image, reducing local installation time and storage requirements.
- **Source Build**: Transitioned the build pipeline to compile natively from the upstream source repository, ensuring better long-term reliability and flexibility.
- **Dynamic Download**: Re-engineered the Dockerfile to dynamically fetch the latest AppImage via the GitHub API, mitigating issues with opaque timestamps in filenames.
- **Debian Migration**: Moved base image to Debian Bookworm to natively resolve `libwebkit2gtk-4.1-0` dependencies.

## 02.07.01.57.2
- Added native healthchecks to accurately reflect container startup state


All notable changes to the App will be documented in this file.

## [02.07.01.57.1] - 2026-06-10
- **Pre-compiled Images**: The add-on now pulls directly from the pre-built `ghcr.io/maziggy/bambu-studio-api` image instead of compiling from source. This eliminates build failures on platforms lacking Git/BuildKit and dramatically speeds up installation.

## [02.07.01.57] - 2026-06-09
- **Upstream Bump**: Updated Bambu Studio base image to version `02.07.01.57` for compatibility with Bambuddy 0.2.4.5.
- **Ubuntu Migration**: Switched the base OS to Ubuntu 22.04 and updated `libwebkit2gtk-4.1-0` to match upstream changes to the AppImage.

## [1.1] - 2026-05-15
- Initial stable release of the dedicated Slicer API sidecar container.
