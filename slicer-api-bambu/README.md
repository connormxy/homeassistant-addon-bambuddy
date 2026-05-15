# Bambuddy Slicer API (Bambu)

A headless Bambu Studio API sidecar container for Bambuddy Auto-Slicing.

This Home Assistant add-on wraps `ghcr.io/maziggy/orca-slicer-api` (bambu variant) so it can be run as a sidecar alongside the Bambuddy add-on.

## Configuration

1. Start this add-on. Make sure port `3001` is exposed in the network settings.
2. In your Bambuddy add-on's Web UI, go to **Settings → Workflow → Slicer**.
3. Turn on **Use Slicer API**.
4. Set the **Sidecar URL** to `http://<your-homeassistant-ip>:3001`.
