<p align="center">
  <img src="https://github.com/connormxy/homeassistant-addon-bambuddy/blob/main/bambuddy/logo.png?raw=true" alt="Bambuddy Logo" width="300">
</p>

# Bambuddy App

[Bambuddy](https://github.com/maziggy/bambuddy) wrapped inside a Homeassistant App.

A self-hosted print archive and management system for Bambu Lab 3D printers.

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg

## Installation

This repository contains a **multi-addon ecosystem** designed to work seamlessly together.

1. **Bambuddy**: The main core application and web interface.
2. **Slicer API (Bambu Studio)**: An optional headless slicing engine for Bambu Studio files.
3. **Slicer API (OrcaSlicer)**: An optional headless slicing engine for OrcaSlicer files.

To use the auto-slicing features of Bambuddy, you must install the Main Add-on **AND** at least one of the Slicer APIs.

## Configuration & Documentation

Please refer to the `Documentation` tab inside the Home Assistant Add-on page after installing, or view the [DOCS.md](./bambuddy/DOCS.md) file directly for detailed explanations of:
*   MQTT Relay Configuration (using `core-mosquitto`)
*   Slicer API routing
*   Database and Security overrides
*   Virtual Printer Setup
